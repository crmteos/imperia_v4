// Imperia v4: Supabase Data Gateway
(function() {
    var config = window.IMPERIA_CONFIG || {};
    
    window.StateGateway = {
        fetchH3Layers: async function() {
            try {
                if (window.supabase && config.SUPABASE_URL && config.SUPABASE_ANON_KEY) {
                    var client = window.supabase.createClient(config.SUPABASE_URL, config.SUPABASE_ANON_KEY);
                    var response = await client.from('h3_spatial_cells').select('*');
                    if (response.data && response.data.length > 0) {
                        return { source: 'supabase', data: response.data };
                    }
                }
            } catch (e) {
                console.warn("Supabase live query failed, falling back to JSON:", e);
            }
            
            // Fallback to static JSON
            var jsonRes = await fetch('./h3_layers.json');
            var jsonData = await jsonRes.json();
            return { source: 'h3_layers.json', data: jsonData };
        }
    };
})();