/**
 * Imperia v4: Supabase Brahman Vault Client Gateway
 */
class BrahmanVaultClient {
    constructor(supabaseUrl, supabaseKey) {
        this.baseUrl = supabaseUrl;
        this.key = supabaseKey;
    }

    async saveInvariant(octave, category, rawSignal, distilledInvariant, score = 0.95, tags = []) {
        const payload = {
            m_octave: octave,
            domain_category: category,
            raw_signal: rawSignal,
            distilled_invariant: distilledInvariant,
            q_coherence_score: score,
            tags: tags
        };

        const response = await fetch(`${this.baseUrl}/rest/v1/brahman_knowledge_vault`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'apikey': this.key,
                'Authorization': `Bearer ${this.key}`,
                'Prefer': 'return=representation'
            },
            body: JSON.stringify(payload)
        });

        return await response.json();
    }
}

if (typeof module !== 'undefined') {
    module.exports = { BrahmanVaultClient };
}