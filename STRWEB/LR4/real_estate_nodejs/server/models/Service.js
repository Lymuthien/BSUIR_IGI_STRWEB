const mongoose = require('mongoose');

const serviceCategorySchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Category name is required'],
    trim: true,
    maxlength: [200, 'Category name cannot exceed 200 characters']
  }
});

const ServiceCategory = mongoose.model('ServiceCategory', serviceCategorySchema);

const serviceSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Service name is required'],
    trim: true,
    maxlength: [200, 'Service name cannot exceed 200 characters']
  },
  category: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'ServiceCategory',
    required: [true, 'Category is required']
  },
  cost: {
    type: Number,
    required: [true, 'Cost is required'],
    min: [0, 'Cost cannot be negative']
  }
}, {
  timestamps: true
});

module.exports.Service = mongoose.model('Service', serviceSchema);
module.exports.ServiceCategory = ServiceCategory;

