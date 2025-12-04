const express = require('express');
const router = express.Router();
const { body, validationResult, query } = require('express-validator');
const Estate = require('../models/Estate');
const { requireAuth, requireRole } = require('../middleware/auth');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { analyzeEstateImage, generateEstateDescription } = require('../utils/aiService');

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../uploads');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, 'estate-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({
  storage: storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|gif/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    
    if (mimetype && extname) {
      return cb(null, true);
    } else {
      cb(new Error('Only image files are allowed'));
    }
  }
});

// Get all estates (public - with search, sort, filter)
router.get('/',
  [
    query('search').optional().trim(),
    query('sortBy').optional().isIn(['cost', 'area', 'createdAt', 'costPerSquareMeter']),
    query('sortOrder').optional().isIn(['asc', 'desc']),
    query('minCost').optional().isNumeric(),
    query('maxCost').optional().isNumeric(),
    query('minArea').optional().isNumeric(),
    query('maxArea').optional().isNumeric(),
    query('status').optional().isIn(['available', 'reserved', 'sold']),
    query('page').optional().isInt({ min: 1 }),
    query('limit').optional().isInt({ min: 1, max: 100 })
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const {
        search,
        sortBy = 'createdAt',
        sortOrder = 'desc',
        minCost,
        maxCost,
        minArea,
        maxArea,
        status,
        page = 1,
        limit = 10
      } = req.query;

      // Build query
      const query = {};

      if (search) {
        query.$or = [
          { address: { $regex: search, $options: 'i' } },
          { description: { $regex: search, $options: 'i' } }
        ];
      }

      if (minCost || maxCost) {
        query.cost = {};
        if (minCost) query.cost.$gte = parseFloat(minCost);
        if (maxCost) query.cost.$lte = parseFloat(maxCost);
      }

      if (minArea || maxArea) {
        query.area = {};
        if (minArea) query.area.$gte = parseFloat(minArea);
        if (maxArea) query.area.$lte = parseFloat(maxArea);
      }

      if (status) {
        query.status = status;
      }

      // Build sort object
      const sort = {};
      sort[sortBy] = sortOrder === 'asc' ? 1 : -1;

      // Execute query
      const skip = (parseInt(page) - 1) * parseInt(limit);
      
      const estates = await Estate.find(query)
        .populate('category', 'name cost')
        .sort(sort)
        .skip(skip)
        .limit(parseInt(limit));

      const total = await Estate.countDocuments(query);

      res.json({
        estates,
        pagination: {
          page: parseInt(page),
          limit: parseInt(limit),
          total,
          pages: Math.ceil(total / parseInt(limit))
        }
      });
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
);

// Get single estate (public)
router.get('/:id', async (req, res) => {
  try {
    const estate = await Estate.findById(req.params.id)
      .populate('category', 'name cost')
      .populate('createdBy', 'firstName lastName email');

    if (!estate) {
      return res.status(404).json({ message: 'Estate not found' });
    }

    res.json(estate);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Create estate (authenticated only)
router.post('/',
  requireAuth,
  upload.single('image'),
  [
    body('address').trim().notEmpty().isLength({ max: 200 }),
    body('cost').isFloat({ min: 0.01 }),
    body('area').isFloat({ min: 0.01 }),
    body('description').trim().notEmpty().isLength({ max: 2000 }),
    body('category').isMongoId(),
    body('rooms').optional().isInt({ min: 0 }),
    body('floor').optional().isInt(),
    body('totalFloors').optional().isInt()
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const estateData = {
        ...req.body,
        createdBy: req.user._id
      };

      // Handle image upload
      if (req.file) {
        estateData.image = `/uploads/${req.file.filename}`;
      }

      // Generate AI description if OpenAI is configured
      if (process.env.OPENAI_API_KEY) {
        try {
          const aiDescription = await generateEstateDescription(estateData);
          if (aiDescription) {
            estateData.aiDescription = aiDescription;
          }
        } catch (error) {
          console.error('Error generating AI description:', error);
        }
      }

      const estate = await Estate.create(estateData);
      const populatedEstate = await Estate.findById(estate._id)
        .populate('category', 'name cost');

      res.status(201).json(populatedEstate);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
);

// Update estate (authenticated only)
router.put('/:id',
  requireAuth,
  upload.single('image'),
  [
    body('address').optional().trim().isLength({ max: 200 }),
    body('cost').optional().isFloat({ min: 0.01 }),
    body('area').optional().isFloat({ min: 0.01 }),
    body('description').optional().trim().isLength({ max: 2000 })
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const estate = await Estate.findById(req.params.id);

      if (!estate) {
        return res.status(404).json({ message: 'Estate not found' });
      }

      // Check if user has permission (must be creator or admin)
      if (estate.createdBy.toString() !== req.user._id.toString() && req.user.role !== 'admin') {
        return res.status(403).json({ message: 'Permission denied' });
      }

      // Handle image upload
      if (req.file) {
        req.body.image = `/uploads/${req.file.filename}`;
      }

      Object.assign(estate, req.body);
      await estate.save();

      const populatedEstate = await Estate.findById(estate._id)
        .populate('category', 'name cost');

      res.json(populatedEstate);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
);

// Delete estate (authenticated only)
router.delete('/:id', requireAuth, async (req, res) => {
  try {
    const estate = await Estate.findById(req.params.id);

    if (!estate) {
      return res.status(404).json({ message: 'Estate not found' });
    }

    // Check if user has permission (must be creator or admin)
    if (estate.createdBy.toString() !== req.user._id.toString() && req.user.role !== 'admin') {
      return res.status(403).json({ message: 'Permission denied' });
    }

    await Estate.findByIdAndDelete(req.params.id);

    res.json({ message: 'Estate deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Analyze estate image with Google Vision AI (authenticated only)
// Can analyze uploaded image or existing estate image
router.post('/:id/analyze-image', requireAuth, upload.single('image'), async (req, res) => {
  try {
    const estate = await Estate.findById(req.params.id);
    if (!estate) {
      return res.status(404).json({ message: 'Estate not found' });
    }

    let imageBase64;

    // If new image uploaded, use it
    if (req.file) {
      const imageBuffer = fs.readFileSync(req.file.path);
      imageBase64 = imageBuffer.toString('base64');
    } 
    // Otherwise, use existing estate image
    else if (estate.image) {
      const imagePath = path.join(__dirname, '..', estate.image);
      if (fs.existsSync(imagePath)) {
        const imageBuffer = fs.readFileSync(imagePath);
        imageBase64 = imageBuffer.toString('base64');
      } else {
        return res.status(404).json({ message: 'Estate image file not found on server' });
      }
    } else {
      return res.status(400).json({ message: 'No image available for analysis. Please upload an image first.' });
    }

    // Analyze with Google Vision AI
    const analysis = await analyzeEstateImage(imageBase64);

    estate.aiAnalysis = analysis;
    await estate.save();

    res.json({
      message: 'Image analyzed successfully',
      analysis
    });
  } catch (error) {
    console.error('Error analyzing image:', error);
    res.status(500).json({ 
      message: error.message || 'Failed to analyze image',
      error: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
});

module.exports = router;

