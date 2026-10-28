// Supabase Client Module - Imperia v4
// Uses native fetch, no npm packages required
// Handles telemetry logging and territory passport retrieval

const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_ANON_KEY = 'your-anon-key';

// Log P2P telemetry to Supabase
export async function log_telemetry(hubId, status, temperature, power, latency, qFactor) {
  try {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/telemetry_logs`, {
      method: 'POST',
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        hub: hubId,
        status: status,
        temperature: temperature,
        power: power,
        latency: latency,
        q_factor: qFactor,
        timestamp: new Date().toISOString()
      })
    });
    
    if (!response.ok) {
      throw new Error(`Supabase error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.warn('Failed to log telemetry to Supabase:', error.message);
    return null;
  }
}

// Read current territory passports
export async function get_territory_passports() {
  try {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/territory_passports`, {
      method: 'GET',
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        'Accept': 'application/json',
      }
    });
    
    if (!response.ok) {
      throw new Error(`Supabase error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.warn('Failed to fetch territory passports:', error.message);
    return [];
  }
}

// Save territory passport
export async function save_territory_passport(passportData) {
  try {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/territory_passports`, {
      method: 'POST',
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(passportData)
    });
    
    if (!response.ok) {
      throw new Error(`Supabase error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.warn('Failed to save territory passport:', error.message);
    return null;
  }
}