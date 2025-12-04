const mongoose = require('mongoose');

const saleSchema = new mongoose.Schema({
  client: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: [true, 'Client is required']
  },
  employee: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: [true, 'Employee is required']
  },
  estate: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Estate',
    required: [true, 'Estate is required'],
    unique: true
  },
  dateOfContract: {
    type: Date,
    default: Date.now,
    required: true
  },
  dateOfSale: {
    type: Date,
    default: Date.now,
    required: true
  },
  estateCost: {
    type: Number,
    required: true,
    min: [0, 'Estate cost cannot be negative']
  },
  serviceCost: {
    type: Number,
    required: true,
    min: [0, 'Service cost cannot be negative']
  },
  totalCost: {
    type: Number,
    required: true,
    min: [0, 'Total cost cannot be negative']
  },
  commission: {
    type: Number,
    default: 0,
    min: [0, 'Commission cannot be negative']
  },
  status: {
    type: String,
    enum: ['pending', 'completed', 'cancelled'],
    default: 'pending'
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

// Calculate total cost before saving
saleSchema.pre('save', function(next) {
  this.totalCost = this.estateCost + this.serviceCost;
  next();
});

// Index for queries
saleSchema.index({ client: 1, status: 1 });
saleSchema.index({ employee: 1, status: 1 });
saleSchema.index({ dateOfSale: -1 });

module.exports = mongoose.model('Sale', saleSchema);

