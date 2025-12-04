const express = require('express');
const router = express.Router();
const { body, validationResult } = require('express-validator');
const Review = require('../models/Review');
const { requireAuth } = require('../middleware/auth');

// Get all reviews (public)
router.get('/', async (req, res) => {
  try {
    const { estate, user, rating, sortBy = 'createdAt', sortOrder = 'desc' } = req.query;
    
    const query = {};
    if (estate) query.estate = estate;
    if (user) query.user = user;
    if (rating) query.rating = parseInt(rating);

    const sort = {};
    sort[sortBy] = sortOrder === 'asc' ? 1 : -1;

    const reviews = await Review.find(query)
      .populate('user', 'firstName lastName email')
      .populate('estate', 'address')
      .sort(sort);

    res.json(reviews);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Get single review
router.get('/:id', async (req, res) => {
  try {
    const review = await Review.findById(req.params.id)
      .populate('user', 'firstName lastName email')
      .populate('estate', 'address');

    if (!review) {
      return res.status(404).json({ message: 'Review not found' });
    }

    res.json(review);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Create review (authenticated only)
router.post('/',
  requireAuth,
  [
    body('rating').isInt({ min: 1, max: 5 }),
    body('text').trim().notEmpty().isLength({ max: 1000 }),
    body('estate').optional().isMongoId()
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const reviewData = {
        ...req.body,
        user: req.user._id
      };

      const review = await Review.create(reviewData);
      const populatedReview = await Review.findById(review._id)
        .populate('user', 'firstName lastName email')
        .populate('estate', 'address');

      res.status(201).json(populatedReview);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
);

// Update review (authenticated - own review only)
router.put('/:id',
  requireAuth,
  [
    body('rating').optional().isInt({ min: 1, max: 5 }),
    body('text').optional().trim().isLength({ max: 1000 })
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const review = await Review.findById(req.params.id);

      if (!review) {
        return res.status(404).json({ message: 'Review not found' });
      }

      // Check if user owns the review
      if (review.user.toString() !== req.user._id.toString()) {
        return res.status(403).json({ message: 'Permission denied' });
      }

      Object.assign(review, req.body);
      await review.save();

      const populatedReview = await Review.findById(review._id)
        .populate('user', 'firstName lastName email')
        .populate('estate', 'address');

      res.json(populatedReview);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
);

// Delete review (authenticated - own review only)
router.delete('/:id', requireAuth, async (req, res) => {
  try {
    const review = await Review.findById(req.params.id);

    if (!review) {
      return res.status(404).json({ message: 'Review not found' });
    }

    // Check if user owns the review or is admin
    if (review.user.toString() !== req.user._id.toString() && req.user.role !== 'admin') {
      return res.status(403).json({ message: 'Permission denied' });
    }

    await Review.findByIdAndDelete(req.params.id);

    res.json({ message: 'Review deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;

