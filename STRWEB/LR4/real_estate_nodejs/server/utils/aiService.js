const axios = require('axios');

// Google Vision AI - Analyze estate photos
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
    
    // Provide more detailed error messages
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

// OpenAI - Generate estate description
const generateEstateDescription = async (estateData) => {
  if (!process.env.OPENAI_API_KEY) {
    console.warn('OpenAI API key not configured');
    return null;
  }

  try {
    const prompt = `Create an attractive marketing description for a real estate property with the following details:
- Address: ${estateData.address}
- Cost: ${estateData.cost} USD
- Area: ${estateData.area} sqm
- Rooms: ${estateData.rooms || 'N/A'}
- Existing description: ${estateData.description || 'None'}

Write a compelling, professional description in 2-3 sentences that highlights the property's key features and value.`;

    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'system',
            content: 'You are a professional real estate marketing specialist.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        max_tokens: 200,
        temperature: 0.7
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data.choices[0].message.content.trim();
  } catch (error) {
    console.error('OpenAI API Error:', error.response?.data || error.message);
    return null;
  }
};

// OpenAI - Chat bot for consultation
const getConsultationResponse = async (userMessage, context = '') => {
  if (!process.env.OPENAI_API_KEY) {
    console.warn('OpenAI API key not configured');
    return 'AI consultation is not available. Please contact our support team.';
  }

  try {
    const systemMessage = `You are a friendly real estate consultant assistant. Help clients with questions about properties, prices, viewing arrangements, and general real estate inquiries. Be professional, concise, and helpful.`;

    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'system',
            content: systemMessage
          },
          ...(context ? [{ role: 'system', content: `Context: ${context}` }] : []),
          {
            role: 'user',
            content: userMessage
          }
        ],
        max_tokens: 150,
        temperature: 0.8
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data.choices[0].message.content.trim();
  } catch (error) {
    console.error('OpenAI Chat API Error:', error.response?.data || error.message);
    return 'I apologize, but I am currently unable to process your request. Please try again later or contact our support team.';
  }
};

module.exports = {
  analyzeEstateImage,
  generateEstateDescription,
  getConsultationResponse
};

