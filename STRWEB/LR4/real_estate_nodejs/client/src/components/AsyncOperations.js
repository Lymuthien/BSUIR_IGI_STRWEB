import React, { useState, useRef } from 'react';
import '../styles/AsyncOperations.css';

// Компонент для демонстрации асинхронных операций (XMLHttpRequest, setTimeout, Promise)
const AsyncOperations = () => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [notifications, setNotifications] = useState([]);
  const [promiseResults, setPromiseResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const timeoutRefs = useRef([]);

  // XMLHttpRequest - для загрузки с отслеживанием прогресса
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const xhr = new XMLHttpRequest();
    setLoading(true);
    setUploadProgress(0);

    // Отслеживание прогресса
    xhr.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable) {
        const percentComplete = (event.loaded / event.total) * 100;
        setUploadProgress(percentComplete);
      }
    });

    // Обработка завершения
    xhr.addEventListener('load', () => {
      if (xhr.status === 200) {
        addNotification('File uploaded successfully!', 'success');
      } else {
        addNotification('Upload failed!', 'error');
      }
      setLoading(false);
      setUploadProgress(0);
    });

    // Обработка ошибок
    xhr.addEventListener('error', () => {
      addNotification('Upload error occurred!', 'error');
      setLoading(false);
      setUploadProgress(0);
    });

    // Отправка файла (симуляция)
    const formData = new FormData();
    formData.append('file', file);
    
    // Здесь можно отправить на реальный сервер
    // xhr.open('POST', '/api/upload');
    // xhr.send(formData);

    // Симуляция для демонстрации
    setTimeout(() => {
      setUploadProgress(100);
      addNotification('File upload simulated successfully!', 'success');
      setLoading(false);
    }, 2000);
  };

  // setTimeout - для автоматического скрытия уведомлений
  const addNotification = (message, type = 'info') => {
    const id = Date.now();
    const notification = { id, message, type };

    setNotifications(prev => [...prev, notification]);

    // Автоматически скрыть через 5 секунд
    const timeoutId = setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== id));
    }, 5000);

    timeoutRefs.current.push(timeoutId);
  };

  // setTimeout - для периодического обновления данных
  const startPeriodicUpdate = () => {
    const updateData = () => {
      const data = {
        timestamp: new Date().toLocaleTimeString(),
        randomValue: Math.floor(Math.random() * 100)
      };
      addNotification(`Data updated: ${data.randomValue}`, 'info');
    };

    // Обновлять каждые 3 секунды
    const intervalId = setInterval(updateData, 3000);
    
    // Остановить через 30 секунд
    setTimeout(() => {
      clearInterval(intervalId);
      addNotification('Periodic updates stopped', 'info');
    }, 30000);

    addNotification('Periodic updates started', 'success');
  };

  // setTimeout - для таймера обратного отсчета
  const startCountdown = () => {
    let countdown = 10;
    addNotification(`Countdown started: ${countdown}`, 'info');

    const countdownInterval = setInterval(() => {
      countdown--;
      if (countdown > 0) {
        addNotification(`Countdown: ${countdown}`, 'info');
      } else {
        clearInterval(countdownInterval);
        addNotification('Countdown finished!', 'success');
      }
    }, 1000);
  };

  // Promise - цепочка асинхронных операций
  const executePromiseChain = async () => {
    setLoading(true);
    setPromiseResults([]);

    try {
      // Шаг 1: Проверка документов
      const step1 = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({ step: 1, message: 'Documents checked' });
        }, 1000);
      });
      setPromiseResults(prev => [...prev, step1]);

      // Шаг 2: Подписание
      const step2 = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({ step: 2, message: 'Documents signed' });
        }, 1000);
      });
      setPromiseResults(prev => [...prev, step2]);

      // Шаг 3: Регистрация
      const step3 = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({ step: 3, message: 'Deal registered' });
        }, 1000);
      });
      setPromiseResults(prev => [...prev, step3]);

      // Шаг 4: Расчет комиссии
      const step4 = await new Promise((resolve) => {
        setTimeout(() => {
          resolve({ step: 4, message: 'Commission calculated: $5000' });
        }, 1000);
      });
      setPromiseResults(prev => [...prev, step4]);

      addNotification('Deal processing completed successfully!', 'success');
    } catch (error) {
      addNotification('Error in deal processing: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  // Promise - параллельные запросы
  const executeParallelPromises = async () => {
    setLoading(true);
    setPromiseResults([]);

    try {
      const promises = [
        Promise.resolve({ source: 'API 1', data: 'Estate data loaded' }),
        Promise.resolve({ source: 'API 2', data: 'Client data loaded' }),
        Promise.resolve({ source: 'API 3', data: 'Service data loaded' })
      ];

      const results = await Promise.all(promises);
      setPromiseResults(results);
      addNotification('All parallel requests completed!', 'success');
    } catch (error) {
      addNotification('Error in parallel requests: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const clearNotifications = () => {
    timeoutRefs.current.forEach(clearTimeout);
    timeoutRefs.current = [];
    setNotifications([]);
  };

  return (
    <div className="async-operations">
      <h3>Asynchronous Operations Demo</h3>

      <div className="operations-grid">
        {/* XMLHttpRequest Section */}
        <div className="operation-section">
          <h4>XMLHttpRequest - File Upload with Progress</h4>
          <input
            type="file"
            onChange={handleFileUpload}
            className="form-control mb-2"
            disabled={loading}
          />
          {uploadProgress > 0 && (
            <div className="progress">
              <div
                className="progress-bar"
                role="progressbar"
                style={{ width: `${uploadProgress}%` }}
              >
                {uploadProgress.toFixed(0)}%
              </div>
            </div>
          )}
        </div>

        {/* setTimeout Section */}
        <div className="operation-section">
          <h4>setTimeout - Timers & Updates</h4>
          <button onClick={startPeriodicUpdate} className="btn btn-primary me-2">
            Start Periodic Updates
          </button>
          <button onClick={startCountdown} className="btn btn-secondary">
            Start Countdown
          </button>
        </div>

        {/* Promise Section */}
        <div className="operation-section">
          <h4>Promise - Async Chains</h4>
          <button 
            onClick={executePromiseChain} 
            className="btn btn-success me-2"
            disabled={loading}
          >
            Execute Deal Chain
          </button>
          <button 
            onClick={executeParallelPromises}
            className="btn btn-info"
            disabled={loading}
          >
            Parallel Requests
          </button>
        </div>
      </div>

      {/* Promise Results */}
      {promiseResults.length > 0 && (
        <div className="promise-results mt-3">
          <h5>Promise Results:</h5>
          <ul>
            {promiseResults.map((result, index) => (
              <li key={index}>
                {result.step && `Step ${result.step}: `}
                {result.source && `${result.source}: `}
                {result.message || result.data}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Notifications */}
      {notifications.length > 0 && (
        <div className="notifications-container">
          <div className="notifications-header">
            <h5>Notifications</h5>
            <button onClick={clearNotifications} className="btn btn-sm btn-secondary">
              Clear All
            </button>
          </div>
          <div className="notifications-list">
            {notifications.map(notification => (
              <div
                key={notification.id}
                className={`notification notification-${notification.type}`}
              >
                {notification.message}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AsyncOperations;

