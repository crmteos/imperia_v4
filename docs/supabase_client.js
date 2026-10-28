// Supabase Client Module - Imperia v4
// Uses native fetch, no npm packages required
// Handles telemetry logging and territory passport retrieval

window.SupabaseClient = window.SupabaseClient || {};

// Log P2P telemetry to Supabase
window.SupabaseClient.log_telemetry = async function(hubId, status, temperature, power, latency, qFactor) {
  try {
    const response = await fetch(\/rest/v1/telemetry_logs\, {
      method: 'POST',
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': \Bearer \,
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
      throw new Error(\Supabase error: \);
    }
    
    return await response.json();
  } catch (error) {
    console.warn('Failed to log telemetry to Supabase:', error.message);
    return null;
  }
};

// Read current territory passports
window.SupabaseClient.get_territory_passports = async function() {
  try {
    const response = await fetch(\/rest/v1/territory_passports\, {
      method: 'GET',
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': \Bearer \,
        'Accept': 'application/json',
      }
    });
    
    if (!response.ok) {
      throw new Error(\Supabase error: \);
    }
    
    return await response.json();
  } catch (error) {
    console.warn('Failed to fetch territory passports:', error.message);
    return [];
  }
};

// Save territory passport
window.SupabaseClient.save_territory_passport = async function(passportData) {
  try {
    const response = await fetch(\/rest/v1/territory_passports\, {
      method: 'POST',
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': \Bearer \,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(passportData)
    });
    
    if (!response.ok) {
      throw new Error(\Supabase error: \);
    }
    
    return await response.json();
  } catch (error) {
    console.warn('Failed to save territory passport:', error.message);
    return null;
  }
};
