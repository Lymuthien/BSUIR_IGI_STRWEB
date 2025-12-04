import { formatInTimeZone } from 'date-fns-tz';
import { format as formatDate } from 'date-fns';

export const getUserTimezone = () => {
  return Intl.DateTimeFormat().resolvedOptions().timeZone;
};

export const formatDateWithTimezone = (date, formatStr = "yyyy-MM-dd HH:mm:ss") => {
  if (!date) return '';
  const d = new Date(date);
  const userTimezone = getUserTimezone();
  return formatInTimeZone(d, userTimezone, formatStr);
};

export const formatDateUTC = (date, formatStr = "yyyy-MM-dd HH:mm:ss") => {
  if (!date) return '';
  const d = new Date(date);
  return formatInTimeZone(d, 'UTC', formatStr);
};

export const getCurrentDateTime = () => {
  const now = new Date();
  return {
    utc: formatDateUTC(now),
    local: formatDateWithTimezone(now),
    timezone: getUserTimezone(),
    timestamp: now.getTime()
  };
};

export const formatRelativeTime = (date) => {
  if (!date) return '';
  const d = new Date(date);
  const now = new Date();
  const diffInSeconds = Math.floor((now - d) / 1000);

  if (diffInSeconds < 60) return 'just now';
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
  
  return formatDate(d, 'MMM dd, yyyy');
};

