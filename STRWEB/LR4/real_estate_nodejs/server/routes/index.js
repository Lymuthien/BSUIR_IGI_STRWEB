const express = require('express');
const router = express.Router();
const { format } = require('date-fns');
const { format: formatTZ, utcToZonedTime } = require('date-fns-tz');

// Health check and server info
router.get('/', (req, res) => {
  const now = new Date();
  const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const zonedDate = utcToZonedTime(now, userTimezone);

  res.json({
    message: 'Real Estate Agency API',
    serverTime: {
      utc: format(now, "yyyy-MM-dd'T'HH:mm:ss.SSSxxx"),
      userTimezone: formatTZ(zonedDate, "yyyy-MM-dd'T'HH:mm:ss.SSSxxx", { timeZone: userTimezone }),
      timezone: userTimezone
    },
    endpoints: {
      auth: '/api/auth',
      estates: '/api/estates',
      reviews: '/api/reviews',
      sales: '/api/sales',
      ai: '/api/ai'
    }
  });
});

module.exports = router;

