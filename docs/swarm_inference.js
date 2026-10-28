// Swarm Inference Module - Imperia v4
// Free OpenRouter API integration for 4D-environment vector calculation

const OPENROUTER_API_KEY = 'your-openrouter-api-key';
const OPENROUTER_ENDPOINT = 'https://openrouter.ai/api/v1';

// Calculate 4D environment vector E = [E_lang, E_geo, E_hist, E_soc]^T
export async function calculateEVector(hubId, geoData) {
  try {
    // Select appropriate model based on availability
    const model = 'nvidia/nemotron-3.5-lightning-free';
    
    const response = await fetch(`${OPENROUTER_ENDPOINT}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': window.location.origin,
        'X-Title': 'Imperia v4'
      },
      body: JSON.stringify({
        model: model,
        messages: [
          {
            role: "system",
            content: "You are an environmental analysis expert. Calculate the 4D environment vector E = [E_lang, E_geo, E_hist, E_soc] for the given location and context. Return ONLY a JSON object with exactly these four numeric values, no other text, no markdown, no explanation."
          },
          {
            role: "user",
            content: `Calculate the 4D environment vector for hub ${hubId} with geographical data: ${JSON.stringify(geoData)}. Return format: {"E_lang": number, "E_geo": number, "E_hist": number, "E_soc": number}`
          }
        ],
        max_tokens: 100,
        temperature: 0.3
      })
    });
    
    if (!response.ok) {
      throw new Error(`OpenRouter error: ${response.status}`);
    }
    
    const data = await response.json();
    const content = data.choices[0].message.content;
    
    // Parse the JSON response
    const vector = JSON.parse(content.trim());
    
    // Validate required fields
    if (vector.E_lang === undefined || vector.E_geo === undefined || 
        vector.E_hist === undefined || vector.E_soc === undefined) {
      throw new Error('Invalid vector format from OpenRouter');
    }
    
    return {
      E_lang: parseFloat(vector.E_lang),
      E_geo: parseFloat(vector.E_geo),
      E_hist: parseFloat(vector.E_hist),
      E_soc: parseFloat(vector.E_soc)
    };
    
  } catch (error) {
    console.warn('OpenRouter calculation failed, using fallback:', error.message);
    // Fallback vector based on basic heuristics
    return {
      E_lang: 0.5,
      E_geo: 0.5,
      E_hist: 0.5,
      E_soc: 0.5
    };
  }
}

// Get weather/sensor data from Open-Meteo
export async function get_weather_data(lat, lon) {
  try {
    const response = await fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m`
    );
    
    if (!response.ok) {
      throw new Error(`Open-Meteo error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.warn('Failed to fetch weather data:', error.message);
    return null;
  }
}

// Estimate socio-economic factor based on hub data
export function estimateSocioEconomic(hubData) {
  // Simple heuristic based on available hub data
  if (!hubData) return 0.5;
  
  let score = 0.5;
  if (hubData.population) score += 0.1;
  if (hubData.incomeLevel) score += 0.1;
  if (hubData.infrastructure) score += 0.1;
  if (hubData.connectivity) score += 0.1;
  
  return Math.min(Math.max(score, 0), 1);
}