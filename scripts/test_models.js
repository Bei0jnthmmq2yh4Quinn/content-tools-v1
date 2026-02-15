const https = require('https');
const http = require('http');

const PROVIDERS = {
  'openai-custom': {
    baseUrl: 'https://api.003636.xyz/v1',
    apiKey: 'sk-ALcXWoPzxJcneU1Hr2ftUux5AfketFOQOoveAUWQqmAFUAVw'
  },
  'anyrouter': {
    baseUrl: 'https://anyrouter.top',
    apiKey: 'sk-free'
  },
  'anthropic-custom': {
    baseUrl: 'https://api.003636.xyz/v1',
    apiKey: 'sk-ALcXWoPzxJcneU1Hr2ftUux5AfketFOQOoveAUWQqmAFUAVw'
  },
  'google': {
    baseUrl: 'https://api.003636.xyz/v1',
    apiKey: 'sk-ALcXWoPzxJcneU1Hr2ftUux5AfketFOQOoveAUWQqmAFUAVw'
  }
};

const MODELS = [
  "openai-custom/gpt-5.2",
  "openai-custom/gemini-3-pro-preview",
  "anthropic-custom/claude-opus-4-5",
  "google/Gemini-3-Pro-Preview",
  "openai-custom/gpt-5",
  "openai-custom/claude-haiku-4-5",
  "openai-custom/gemini-2.5-pro",
  "openai-custom/gemini-3-pro-image",
  "anyrouter/claude-opus-4-5-20251101",
  "openai-custom/claude-opus-4-6-thinking",
  "openai-custom/celebras/gpt-oss-120b",
  "openai-custom/celebras/qwen-3-32b",
  "openai-custom/celebras/zai-glm-4.7",
  "openai-custom/claude-opus-4-20250514-thinking",
  "openai-custom/claude-opus-4-5",
  "openai-custom/claude-sonnet-4-20250514-thinking",
  "openai-custom/claude-sonnet-4-5",
  "openai-custom/claude-sonnet-4-5-thinking",
  "openai-custom/deepseek-ai/DeepSeek-V3.2",
  "openai-custom/gemini-2.5-flash",
  "openai-custom/gemini-2.5-flash-lite",
  "openai-custom/gemini-3-flash",
  "openai-custom/gemini-3-flash-preview",
  "openai-custom/gemini-3-pro-high",
  "openai-custom/gemini-flash-latest",
  "openai-custom/gemini-flash-lite-latest",
  "openai-custom/gpt-5-codex",
  "openai-custom/gpt-5-codex-mini",
  "openai-custom/gpt-5-nano",
  "openai-custom/gpt-5.1",
  "openai-custom/gpt-5.1-codex",
  "openai-custom/gpt-5.1-codex-max",
  "openai-custom/gpt-5.1-codex-mini",
  "openai-custom/gpt-5.2-codex",
  "openai-custom/gpt-5.3-codex",
  "openai-custom/gpt-oss-120b-medium",
  "openai-custom/monica/claude-4-sonnet",
  "openai-custom/monica/claude-4-sonnet-thinking",
  "openai-custom/monica/claude-sonnet-4-5",
  "openai-custom/monica/gemini-2.5-pro",
  "openai-custom/monica/gemini-3-pro-preview-thinking",
  "openai-custom/monica/gpt-4.1",
  "openai-custom/monica/gpt-5",
  "openai-custom/monica/grok-4",
  "openai-custom/monica/o3",
  "openai-custom/nebius/DeepSeek-R1-0528-fast",
  "openai-custom/nebius/deepseek-ai/DeepSeek-V3-0324-fast",
  "openai-custom/nebius/glm-4.5",
  "openai-custom/nebius/gpt-oss-120b",
  "openai-custom/nebius/qwen3-235B-2507",
  "openai-custom/nyxar/claude-sonnet-4-20250514",
  "openai-custom/nyxar/gpt-5",
  "openai-custom/nyxar/gpt-oss-120b",
  "openai-custom/oaipro/claude-opus-4-20250514",
  "openai-custom/oaipro/claude-sonnet-4-20250514",
  "openai-custom/oaipro/gpt-4.1",
  "openai-custom/oaipro/gpt-5",
  "openai-custom/oaipro/o1",
  "openai-custom/oaipro/o3",
  "openai-custom/ohmygpt/chatgpt-4o-latest",
  "openai-custom/ohmygpt/claude-opus-4-1",
  "openai-custom/ohmygpt/claude-opus-4-20250514",
  "openai-custom/ohmygpt/claude-sonnet-4-20250514",
  "openai-custom/ohmygpt/gemini-2.5-pro",
  "openai-custom/ohmygpt/glm-4.5",
  "openai-custom/ohmygpt/gpt-4.1",
  "openai-custom/ohmygpt/gpt-5",
  "openai-custom/ohmygpt/grok-4-latest",
  "openai-custom/ohmygpt/o3",
  "openai-custom/zai-org/GLM-4.7-FP8",
  "openai-custom/官代/gpt-4.1",
  "openai-custom/官代/gpt-5-mini",
  "openai-custom/官代/o1",
  "openai-custom/官代/o3",
  "openai-custom/硅基/Qwen/Qwen3-235B-A22B-Thinking-2507",
  "openai-custom/硅基/Qwen/Qwen3-Coder-480B-A35B-Instruct",
  "openai-custom/硅基/deepseek-ai/DeepSeek-V3.1",
  "openai-custom/硅基/moonshotai/Kimi-K2-Instruct",
  "openai-custom/硅基/zai-org/GLM-4.5V",
  "openai-custom/gpt-5.2-high"
];

function testModel(fullModel) {
  return new Promise((resolve) => {
    const [provider, ...rest] = fullModel.split('/');
    const modelId = rest.join('/');
    const providerConfig = PROVIDERS[provider];
    
    if (!providerConfig) {
      resolve({ model: fullModel, ok: false, error: 'Unknown provider: ' + provider });
      return;
    }

    const url = new URL(providerConfig.baseUrl + '/chat/completions');
    const isAnthropicMessages = provider === 'anyrouter';
    
    const body = JSON.stringify({
      model: modelId,
      messages: [{ role: 'user', content: 'Hi' }],
      max_tokens: 5,
      stream: false
    });

    const options = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${providerConfig.apiKey}`,
        'Content-Length': Buffer.byteLength(body)
      },
      timeout: 30000
    };

    const client = url.protocol === 'https:' ? https : http;
    const req = client.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.error) {
            resolve({ model: fullModel, ok: false, error: json.error.message || JSON.stringify(json.error).slice(0, 100) });
          } else if (json.choices && json.choices.length > 0) {
            resolve({ model: fullModel, ok: true });
          } else {
            resolve({ model: fullModel, ok: false, error: 'No choices in response' });
          }
        } catch (e) {
          resolve({ model: fullModel, ok: false, error: 'Parse error: ' + data.slice(0, 100) });
        }
      });
    });

    req.on('error', (e) => {
      resolve({ model: fullModel, ok: false, error: e.message });
    });

    req.on('timeout', () => {
      req.destroy();
      resolve({ model: fullModel, ok: false, error: 'Timeout' });
    });

    req.write(body);
    req.end();
  });
}

async function runTests() {
  const results = { ok: [], fail: [] };
  const concurrency = 5;
  let idx = 0;

  async function worker() {
    while (idx < MODELS.length) {
      const model = MODELS[idx++];
      const result = await testModel(model);
      if (result.ok) {
        results.ok.push(result.model);
        process.stdout.write('✓');
      } else {
        results.fail.push({ model: result.model, error: result.error });
        process.stdout.write('✗');
      }
    }
  }

  const workers = [];
  for (let i = 0; i < concurrency; i++) {
    workers.push(worker());
  }
  await Promise.all(workers);

  console.log('\n\n=== RESULTS ===');
  console.log(`\n✅ OK (${results.ok.length}):`);
  results.ok.forEach(m => console.log('  ' + m));
  console.log(`\n❌ FAIL (${results.fail.length}):`);
  results.fail.forEach(r => console.log('  ' + r.model + ' — ' + r.error));
}

runTests();
