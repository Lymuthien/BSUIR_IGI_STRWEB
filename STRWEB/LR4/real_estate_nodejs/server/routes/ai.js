const express = require('express');
const router = express.Router();
const { body, validationResult } = require('express-validator');
const { getConsultationResponse } = require('../utils/aiService');
const { requireAuth } = require('../middleware/auth');

// AI Chat consultation (authenticated only)
router.post('/consultation',
  requireAuth,
  [
    body('message').trim().notEmpty().isLength({ max: 500 }),
    body('context').optional().trim()
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const { message, context } = req.body;

      const response = await getConsultationResponse(message, context);

      res.json({
        response,
        timestamp: new Date()
      });
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
);

module.exports = router;

