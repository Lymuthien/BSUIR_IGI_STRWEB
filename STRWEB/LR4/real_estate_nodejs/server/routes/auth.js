const express = require('express');
const router = express.Router();
const passport = require('passport');
const { body, validationResult } = require('express-validator');
const User = require('../models/User');
const { requireAuth } = require('../middleware/auth');

// Register
router.post('/register',
  [
    body('email').isEmail().normalizeEmail(),
    body('password').isLength({ min: 6 }),
    body('firstName').trim().notEmpty(),
    body('lastName').trim().notEmpty(),
    body('role').optional().isIn(['client', 'employee'])
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const { email, password, firstName, lastName, role = 'client', phoneNumber, birthDate } = req.body;

      // Check if user exists
      const existingUser = await User.findOne({ email });
      if (existingUser) {
        return res.status(400).json({ message: 'User already exists' });
      }

      // Create username from email
      const username = email.split('@')[0];

      // Create user
      const user = await User.create({
        email,
        password,
        username,
        firstName,
        lastName,
        role,
        phoneNumber,
        birthDate
      });

      // Log in user
      req.login(user, (err) => {
        if (err) {
          return res.status(500).json({ message: 'Error during login' });
        }
        return res.status(201).json({
          message: 'Registration successful',
          user: {
            id: user._id,
            email: user.email,
            firstName: user.firstName,
            lastName: user.lastName,
            role: user.role
          }
        });
      });
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }
);

// Login
router.post('/login',
  passport.authenticate('local', { failureFlash: false }),
  (req, res) => {
    res.json({
      message: 'Login successful',
      user: {
        id: req.user._id,
        email: req.user.email,
        firstName: req.user.firstName,
        lastName: req.user.lastName,
        role: req.user.role
      }
    });
  }
);

// Logout
router.post('/logout', (req, res) => {
  req.logout((err) => {
    if (err) {
      return res.status(500).json({ message: 'Error during logout' });
    }
    res.json({ message: 'Logout successful' });
  });
});

// Get current user
router.get('/me', requireAuth, (req, res) => {
  res.json({
    user: {
      id: req.user._id,
      email: req.user.email,
      firstName: req.user.firstName,
      lastName: req.user.lastName,
      role: req.user.role,
      profilePicture: req.user.profilePicture
    }
  });
});

// Google OAuth
router.get('/google',
  passport.authenticate('google', { scope: ['profile', 'email'] })
);

router.get('/google/callback',
  passport.authenticate('google', { failureRedirect: '/login' }),
  (req, res) => {
    // Redirect to frontend with token or user info
    res.redirect(`${process.env.CLIENT_URL || 'http://localhost:3000'}/auth/success`);
  }
);

module.exports = router;

