const express = require('express');
const router = express.Router();
const { body, validationResult } = require('express-validator');
const Sale = require('../models/Sale');
const Estate = require('../models/Estate');
const Service = require('../models/Service');
const { requireAuth, requireRole } = require('../middleware/auth');

router.get('/', requireAuth, requireRole('employee', 'admin'), async (req, res) => {
  try {
    const { client, employee, status, sortBy = 'dateOfSale', sortOrder = 'desc' } = req.query;
    
    const query = {};
    if (client) query.client = client;
    if (employee) query.employee = employee;
    if (status) query.status = status;

    const sort = {};
    sort[sortBy] = sortOrder === 'asc' ? 1 : -1;

    const sales = await Sale.find(query)
      .populate('client', 'firstName lastName email')
      .populate('employee', 'firstName lastName email')
      .populate('estate', 'address cost area')
      .sort(sort);

    res.json(sales);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.get('/my-sales', requireAuth, async (req, res) => {
  try {
    const query = { client: req.user._id };

    const sales = await Sale.find(query)
      .populate('employee', 'firstName lastName email')
      .populate('estate', 'address cost area')
      .sort({ dateOfSale: -1 });

    res.json(sales);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.get('/:id', requireAuth, async (req, res) => {
  try {
    const sale = await Sale.findById(req.params.id)
      .populate('client', 'firstName lastName email')
      .populate('employee', 'firstName lastName email')
      .populate('estate', 'address cost area description');

    if (!sale) {
      return res.status(404).json({ message: 'Sale not found' });
    }

    if (sale.client._id.toString() !== req.user._id.toString() && 
        sale.employee._id.toString() !== req.user._id.toString() && 
        req.user.role !== 'admin') {
      return res.status(403).json({ message: 'Permission denied' });
    }

    res.json(sale);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.post('/',
  requireAuth,
  requireRole('employee', 'admin'),
  [
    body('client').isMongoId(),
    body('estate').isMongoId(),
    body('dateOfContract').optional().isISO8601(),
    body('dateOfSale').optional().isISO8601()
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const { client, estate: estateId, dateOfContract, dateOfSale } = req.body;

      const estate = await Estate.findById(estateId);
      if (!estate) {
        return res.status(404).json({ message: 'Estate not found' });
      }

      if (estate.status === 'sold') {
        return res.status(400).json({ message: 'Estate is already sold' });
      }

      let serviceCost = 0;
      if (estate.category) {
        const service = await Service.findById(estate.category);
        if (service) {
          serviceCost = service.cost;
        }
      }

      const saleData = {
        client,
        employee: req.user._id,
        estate: estateId,
        estateCost: estate.cost,
        serviceCost,
        dateOfContract: dateOfContract || new Date(),
        dateOfSale: dateOfSale || new Date()
      };

      const sale = await Sale.create(saleData);

      estate.status = 'sold';
      await estate.save();

      const populatedSale = await Sale.findById(sale._id)
        .populate('client', 'firstName lastName email')
        .populate('employee', 'firstName lastName email')
        .populate('estate', 'address cost area');

      res.status(201).json(populatedSale);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
);

router.patch('/:id',
  requireAuth,
  requireRole('employee', 'admin'),
  [
    body('status').isIn(['pending', 'completed', 'cancelled'])
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const sale = await Sale.findById(req.params.id);

      if (!sale) {
        return res.status(404).json({ message: 'Sale not found' });
      }

      sale.status = req.body.status;
      await sale.save();

      const populatedSale = await Sale.findById(sale._id)
        .populate('client', 'firstName lastName email')
        .populate('employee', 'firstName lastName email')
        .populate('estate', 'address cost area');

      res.json(populatedSale);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
);

module.exports = router;

