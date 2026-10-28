window.SupabaseClient = {
    logTelemetry: function(data) {
        console.log(Supabase log:, data);
        return Promise.resolve({ success: true });
    },
    getPassports: function() {
        return Promise.resolve([]);
    }}
