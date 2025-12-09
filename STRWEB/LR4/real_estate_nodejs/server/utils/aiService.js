const axios = require('axios');

// Google Vision AI
const analyzeEstateImage = async (imageBase64, imageType = 'image/jpeg') => {
  if (!process.env.GOOGLE_VISION_API_KEY) {
    const error = 'Google Vision API key not configured. Please add GOOGLE_VISION_API_KEY to .env file.';
    console.warn(error);
    throw new Error(error);
  }

  try {
    const response = await axios.post(
      `https://vision.googleapis.com/v1/images:annotate?key=${process.env.GOOGLE_VISION_API_KEY}`,
      {
        requests: [
          {
            image: {
              content: imageBase64
            },
            features: [
              {
                type: 'LABEL_DETECTION',
                maxResults: 10
              },
              {
                type: 'OBJECT_LOCALIZATION',
                maxResults: 10
              },
              {
                type: 'TEXT_DETECTION'
              }
            ]
          }
        ]
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    // Check for errors in response
    if (response.data.responses && response.data.responses[0].error) {
      const error = response.data.responses[0].error;
      throw new Error(`Google Vision API Error: ${error.message || JSON.stringify(error)}`);
    }

    return response.data.responses[0];
  } catch (error) {
    console.error('Google Vision API Error:', error.response?.data || error.message);
    
    if (error.response?.data?.error) {
      const apiError = error.response.data.error;
      if (apiError.code === 400) {
        throw new Error(`Invalid request: ${apiError.message || 'Bad request format'}`);
      } else if (apiError.code === 403) {
        throw new Error(`API key error: ${apiError.message || 'Invalid API key or insufficient permissions'}`);
      } else if (apiError.code === 429) {
        throw new Error(`Rate limit exceeded: ${apiError.message || 'Too many requests. Please try again later.'}`);
      } else {
        throw new Error(`Google Vision API Error: ${apiError.message || JSON.stringify(apiError)}`);
      }
    }
    
    throw error;
  }
};

module.exports = {
  analyzeEstateImage
};

