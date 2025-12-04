const mongoose = require('mongoose');

const estateSchema = new mongoose.Schema({
  address: {
    type: String,
    required: [true, 'Address is required'],
    trim: true,
    maxlength: [200, 'Address cannot exceed 200 characters']
  },
  cost: {
    type: Number,
    required: [true, 'Cost is required'],
    min: [0.01, 'Cost must be greater than 0']
  },
  area: {
    type: Number,
    required: [true, 'Area is required'],
    min: [0.01, 'Area must be greater than 0']
  },
  category: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Service',
    required: true
  },
  description: {
    type: String,
    required: [true, 'Description is required'],
    maxlength: [2000, 'Description cannot exceed 2000 characters']
  },
  image: {
    type: String,
    default: null
  },
  images: [{
    type: String
  }],
  // AI generated description from OpenAI
  aiDescription: {
    type: String
  },
  // AI analysis from Google Vision
  aiAnalysis: {
    type: mongoose.Schema.Types.Mixed
  },
  status: {
    type: String,
    enum: ['available', 'reserved', 'sold'],
    default: 'available'
  },
  rooms: {
    type: Number,
    min: [0, 'Rooms cannot be negative']
  },
  floor: {
    type: Number
  },
  totalFloors: {
    type: Number
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  },
  createdBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }
}, {
  timestamps: true
});

// Index for search functionality
estateSchema.index({ address: 'text', description: 'text' });
estateSchema.index({ cost: 1, area: 1 });
estateSchema.index({ status: 1 });

// Virtual for cost per square meter
estateSchema.virtual('costPerSquareMeter').get(function() {
  if (this.area && this.area > 0) {
    return (this.cost / this.area).toFixed(2);
  }
  return 0;
});

module.exports = mongoose.model('Estate', estateSchema);

