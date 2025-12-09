const express = require('express');
const router = express.Router();
const { Service, ServiceCategory } = require('../models/Service');

router.get('/categories', async (req, res) => {
  try {
    const categories = await ServiceCategory.find().sort({ name: 1 });
    res.json(categories);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.get('/', async (req, res) => {
  try {
    const services = await Service.find()
      .populate('category', 'name')
      .sort({ 'category.name': 1, name: 1 });
    res.json(services);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.get('/:id', async (req, res) => {
  try {
    const service = await Service.findById(req.params.id)
      .populate('category', 'name');

    if (!service) {
      return res.status(404).json({ message: 'Service not found' });
    }

    res.json(service);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;

