import React, { useState, useEffect } from 'react';
import { getCurrentDateTime, formatDateWithTimezone, formatDateUTC } from '../utils/dateUtils';
import '../styles/DateTimeDisplay.css';

// Функциональный компонент со стрелочной функцией
const DateTimeDisplay = ({ label = 'Server Time', date, showTimezone = true }) => {
  const [currentTime, setCurrentTime] = useState(getCurrentDateTime());

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(getCurrentDateTime());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const displayDate = date ? {
    local: formatDateWithTimezone(date),
    utc: formatDateUTC(date),
    timezone: currentTime.timezone
  } : null;

  return (
    <div className="datetime-display">
      {!date && (
        <div className="current-time">
          <div className="time-label">{label}</div>
          {showTimezone && (
            <div className="timezone">Timezone: {currentTime.timezone}</div>
          )}
          <div className="time-local">Local: {currentTime.local}</div>
          <div className="time-utc">UTC: {currentTime.utc}</div>
        </div>
      )}
      {displayDate && (
        <div className="date-info">
          <div className="date-label">{label}</div>
          {showTimezone && (
            <div className="timezone">Timezone: {displayDate.timezone}</div>
          )}
          <div className="date-local">Local: {displayDate.local}</div>
          <div className="date-utc">UTC: {displayDate.utc}</div>
        </div>
      )}
    </div>
  );
};

export default DateTimeDisplay;

