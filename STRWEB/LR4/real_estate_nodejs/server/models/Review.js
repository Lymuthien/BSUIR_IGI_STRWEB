const mongoose = require('mongoose');

const reviewSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: [true, 'User is required']
  },
  rating: {
    type: Number,
    required: [true, 'Rating is required'],
    min: [1, 'Rating must be at least 1'],
    max: [5, 'Rating cannot exceed 5'],
    validate: {
      validator: Number.isInteger,
      message: 'Rating must be an integer'
    }
  },
  text: {
    type: String,
    required: [true, 'Review text is required'],
    maxlength: [1000, 'Review text cannot exceed 1000 characters']
  },
  estate: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Estate'
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
}, {
  timestamps: true
});

// Index for queries
reviewSchema.index({ user: 1 });
reviewSchema.index({ estate: 1 });
reviewSchema.index({ rating: -1, createdAt: -1 });

module.exports = mongoose.model('Review', reviewSchema);

