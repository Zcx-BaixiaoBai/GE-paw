
import { useEffect, useState, useRef } from "react";
import { apiGet, apiPost, apiPut, apiDel } from "../../lib/api";
import { t } from "../../lib/i18n";

interface Provider {
  id: string;
  name: string;
  base_url: string;
  api_key?: string;
  chat_model?: string;
  generate_kwargs?: Record<string, any>;
  custom_headers?: Record<string, string>;
  auth_mode?: string;
  is_configured?: boolean;
  is_active?: boolean;
}

interface ProviderConfig {
  base_url: string;
  api_key: string;
  model: string;
  temperature: number;
  max_tokens: number;
  top_p: number;
  custom_headers: Record<string, string>;
  auth_mode: "api_key" | "auth_token";
}

const PRESET_PROVIDERS = [
  {
    id: "openai",
    name: "OpenAI",
    emoji: "🔵",
    defaultBaseUrl: "https://api.openai.com/v1",
    defaultModel: "gpt-4o-mini",
    popularModels: ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
  },
  {
    id: "anthropic",
    name: "Anthropic",
    emoji: "🟠",
    defaultBaseUrl: "https://api.anthropic.com/v1",
    defaultModel: "claude-3-5-sonnet-20241022",
    popularModels: ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"]
  },
  {
    id: "google",
    name: "Google Gemini",
    emoji: "🔴",
    defaultBaseUrl: "https://generativelanguage.googleapis.com/v1beta",
    defaultModel: "gemini-pro",
    popularModels: ["gemini-pro", "gemini-pro-vision", "gemini-1.5-pro", "gemini-1.5-flash"]
  },
  {
    id: "deepseek",
    name: "DeepSeek",
    emoji: "🟣",
    defaultBaseUrl: "https://api.deepseek.com",
    defaultModel: "deepseek-chat",
    popularModels: ["deepseek-chat", "deepseek-coder", "deepseek-reasoner"]
  },
  {
    id: "qwen",
    name: "Qwen",
    emoji: "🟡",
    defaultBaseUrl: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    defaultModel: "qwen-turbo",
    popularModels: ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-long"]
  },
  {
    id: "moonshot",
    name: "Moonshot",
    emoji: "🌙",
    defaultBaseUrl: "https://api.moonshot.cn/v1",
    defaultModel: "moonshot-v1-8k",
    popularModels: ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"]
  },
  {
    id: "zhipu",
    name: "ZhipuGLM",
    emoji: "🟤",
    defaultBaseUrl: "https://open.bigmodel.cn/api/paas/v4",
    defaultModel: "glm-4",
    popularModels: ["glm-4", "glm-4v", "glm-3-turbo"]
  }
];

const EMPTY_CONFIG: ProviderConfig = {
  base_url: "",
  api_key: "",
  model: "",
  temperature: 0.7,
  max_tokens: 4096,
  top_p: 1,
  custom_headers: {},
  auth_mode: "api_key"
};

export function AdminLLMPage() {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [activeProvider, setActiveProvider] = useState<string | null>(null);
  const [selectedProvider, setSelectedProvider] = useState<string | null>(null);
  const [config, setConfig] = useState<ProviderConfig>({ ...EMPTY_CONFIG });
  const [loading, setLoading] = useState(false);
  const [testing, setTesting] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const headersRef = useRef<Record<string, string>>({});

  useEffect(() => {
    loadProviders();
  }, []);

  useEffect(() => {
    if (selectedProvider) {
      loadProviderConfig(selectedProvider);
    }
  }, [selectedProvider]);

  async function loadProviders() {
    try {
      const data = await apiGet<Provider[]>("/admin/llm/providers");
      setProviders(data);
      const active = data.find(p => p.is_active);
      if (active) {
        setActiveProvider(active.id);
        if (!selectedProvider) {
          setSelectedProvider(active.id);
        }
      }
    } catch (e: any) {
      console.error("Failed to load providers:", e);
    }
  }

  async function loadProviderConfig(providerId: string) {
    try {
      const provider = providers.find(p => p.id === providerId);
      if (provider && provider.is_configured) {
        setConfig({
          base_url: provider.base_url || "",
          api_key: provider.api_key || "",
          model: provider.chat_model || "",
          temperature: provider.generate_kwargs?.temperature || 0.7,
          max_tokens: provider.generate_kwargs?.max_tokens || 4096,
          top_p: provider.generate_kwargs?.top_p || 1,
          custom_headers: provider.custom_headers || {},
          auth_mode: (provider.auth_mode as "api_key" | "auth_token") || "api_key"
        });
        headersRef.current = provider.custom_headers || {};
      } else {
        const preset = PRESET_PROVIDERS.find(p => p.id === providerId);
        if (preset) {
          setConfig({
            ...EMPTY_CONFIG,
            base_url: preset.defaultBaseUrl,
            model: preset.defaultModel
          });
          headersRef.current = {};
        } else {
          setConfig({ ...EMPTY_CONFIG });
          headersRef.current = {};
        }
      }
    } catch (e: any) {
      console.error("Failed to load provider config:", e);
    }
  }

  async function saveConfig() {
    if (!selectedProvider) return;
    
    setLoading(true);
    setMessage(null);
    
    try {
      const payload = {
        base_url: config.base_url || undefined,
        api_key: config.api_key || undefined,
        chat_model: config.model || undefined,
        generate_kwargs: {
          temperature: config.temperature,
          max_tokens: config.max_tokens,
          top_p: config.top_p
        },
        custom_headers: Object.keys(headersRef.current).length > 0 ? headersRef.current : undefined,
        auth_mode: config.auth_mode
      };

      await apiPut(`/admin/llm/providers/${selectedProvider}/config`, payload);
      
      setMessage({ type: "success", text: t("admin.llm.saveSuccess") });
      loadProviders();
      
      setTimeout(() => setMessage(null), 3000);
    } catch (e: any) {
      setMessage({ type: "error", text: e?.message || t("admin.llm.saveFailed") });
    } finally {
      setLoading(false);
    }
  }

  async function testConnection() {
    if (!selectedProvider) return;
    
    setTesting(true);
    setMessage(null);
    
    try {
      const payload = {
        api_key: config.api_key || undefined,
        base_url: config.base_url || undefined,
        custom_headers: Object.keys(headersRef.current).length > 0 ? headersRef.current : undefined,
        auth_mode: config.auth_mode
      };

      const result = await apiPost(`/admin/llm/providers/${selectedProvider}/test`, payload);
      
      if (result.success) {
        setMessage({ type: "success", text: t("admin.llm.testSuccess") });
      } else {
        setMessage({ type: "error", text: result.message || t("admin.llm.testFailed") });
      }
      
      setTimeout(() => setMessage(null), 5000);
    } catch (e: any) {
      setMessage({ type: "error", text: e?.message || t("admin.llm.testFailed") });
    } finally {
      setTesting(false);
    }
  }

  async function deleteProvider() {
    if (!selectedProvider) return;
    
    setDeleting(true);
    setMessage(null);
    
    try {
      await apiDel(`/admin/llm/providers/${selectedProvider}`);
      
      setMessage({ type: "success", text: t("admin.llm.deleteSuccess") });
      setSelectedProvider(null);
      loadProviders();
      
      setTimeout(() => setMessage(null), 3000);
    } catch (e: any) {
      setMessage({ type: "error", text: e?.message || t("admin.llm.deleteFailed") });
    } finally {
      setDeleting(false);
      setShowDeleteConfirm(false);
    }
  }

  async function setActiveModel() {
    if (!selectedProvider) return;
    
    try {
      const preset = PRESET_PROVIDERS.find(p => p.id === selectedProvider);
      if (!preset) return;
      
      await apiPut("/admin/llm/active", {
        provider_id: selectedProvider,
        model: config.model || preset.defaultModel,
        scope: "global"
      });
      
      setActiveProvider(selectedProvider);
      loadProviders();
    } catch (e: any) {
      console.error("Failed to set active model:", e);
    }
  }

  function addHeader() {
    const key = prompt(t("admin.llm.headerKey"));
    if (!key) return;
    
    const value = prompt(t("admin.llm.headerValue"));
    if (value === null) return;
    
    headersRef.current = { ...headersRef.current, [key]: value };
    setConfig({ ...config, custom_headers: { ...headersRef.current } });
  }

  function removeHeader(key: string) {
    const { [key]: _, ...rest } = headersRef.current;
    headersRef.current = rest;
    setConfig({ ...config, custom_headers: { ...rest } });
  }

  function isProviderConfigured(providerId: string) {
    const provider = providers.find(p => p.id === providerId);
    return provider?.is_configured || false;
  }

  function isActiveProvider(providerId: string) {
    return activeProvider === providerId;
  }

  const selectedPreset = PRESET_PROVIDERS.find(p => p.id === selectedProvider);
  const isConfigured = selectedProvider ? isProviderConfigured(selectedProvider) : false;

  return (
    <div className="admin-page">
      <h1>{t("admin.llm.title")}</h1>
      
      {message && (
        <div className={`admin-card ${message.type === "error" ? "admin-err" : "admin-success"}`}>
          {message.text}
        </div>
      )}

      {/* 供应商网格 */}
      <div style={{ marginBottom: "24px" }}>
        <h2 style={{ marginBottom: "16px", fontSize: "18px" }}>{t("admin.llm.providers")}</h2>
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))",
          gap: "12px"
        }}>
          {PRESET_PROVIDERS.map((preset) => {
            const configured = isProviderConfigured(preset.id);
            const active = isActiveProvider(preset.id);
            
            return (
              <div
                key={preset.id}
                onClick={() => setSelectedProvider(preset.id)}
                style={{
                  background: "var(--bg-elevated)",
                  border: `1px solid ${selectedProvider === preset.id ? "var(--accent)" : "var(--border)"}`,
                  borderRadius: "12px",
                  padding: "20px 24px",
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                  borderLeft: active ? "4px solid var(--accent)" : undefined,
                  boxShadow: selectedProvider === preset.id ? "0 0 0 3px var(--accent-soft)" : undefined
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "12px" }}>
                  <span style={{ fontSize: "24px" }}>{preset.emoji}</span>
                  <div>
                    <div style={{ fontWeight: "600", fontSize: "16px" }}>{preset.name}</div>
                    <div style={{ fontSize: "12px", color: "var(--text-secondary)" }}>
                      {configured ? (
                        <span style={{ color: "var(--success)" }}>{t("admin.llm.configured")}</span>
                      ) : (
                        <span style={{ color: "var(--text-secondary)" }}>{t("admin.llm.notConfigured")}</span>
                      )}
                    </div>
                  </div>
                </div>
                {active && (
                  <div style={{
                    fontSize: "12px",
                    color: "var(--accent)",
                    fontWeight: "500",
                    marginTop: "8px"
                  }}>
                    {t("admin.llm.active")}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* 配置面板 */}
      {selectedProvider && (
        <div style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border)",
          borderRadius: "12px",
          padding: "20px 24px",
          marginBottom: "24px"
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
            <h2 style={{ margin: 0, fontSize: "18px" }}>
              {selectedPreset?.emoji} {selectedPreset?.name} - {t("admin.llm.selectProvider")}
            </h2>
            <div style={{ display: "flex", gap: "12px" }}>
              {isConfigured && (
                <button
                  onClick={() => setShowDeleteConfirm(true)}
                  style={{
                    background: "transparent",
                    border: "1px solid var(--border)",
                    borderRadius: "8px",
                    padding: "8px 16px",
                    cursor: "pointer",
                    color: "var(--danger)"
                  }}
                  disabled={deleting}
                >
                  {deleting ? "删除中..." : t("admin.llm.delete")}
                </button>
              )}
              <button
                onClick={testConnection}
                style={{
                  background: "transparent",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  padding: "8px 16px",
                  cursor: "pointer"
                }}
                disabled={testing}
              >
                {testing ? "测试中..." : t("admin.llm.test")}
              </button>
              <button
                onClick={saveConfig}
                style={{
                  background: "var(--accent)",
                  color: "white",
                  border: "none",
                  borderRadius: "8px",
                  padding: "8px 16px",
                  cursor: "pointer",
                  fontWeight: "500"
                }}
                disabled={loading}
              >
                {loading ? "保存中..." : t("admin.llm.save")}
              </button>
            </div>
          </div>

          {/* 基础配置 */}
          <div style={{ display: "grid", gap: "16px", marginBottom: "20px" }}>
            <div style={{ display: "grid", gap: "12px" }}>
              <label style={{ display: "block" }}>
                <span style={{ display: "block", marginBottom: "8px", fontWeight: "500" }}>
                  {t("admin.llm.baseUrl")}
                </span>
                <input
                  type="text"
                  value={config.base_url}
                  onChange={(e) => setConfig({ ...config, base_url: e.target.value })}
                  placeholder={selectedPreset?.defaultBaseUrl}
                  style={{
                    width: "100%",
                    background: "var(--bg)",
                    border: "1px solid var(--border)",
                    borderRadius: "8px",
                    padding: "8px 12px",
                    fontSize: "14px",
                    outline: "none",
                    transition: "all 0.2s ease"
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = "var(--accent)";
                    e.target.style.boxShadow = "0 0 0 3px var(--accent-soft)";
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = "var(--border)";
                    e.target.style.boxShadow = "none";
                  }}
                />
              </label>

              <label style={{ display: "block" }}>
                <span style={{ display: "block", marginBottom: "8px", fontWeight: "500" }}>
                  {t("admin.llm.apiKey")}
                </span>
                <div style={{ position: "relative" }}>
                  <input
                    type={showPassword ? "text" : "password"}
                    value={config.api_key}
                    onChange={(e) => setConfig({ ...config, api_key: e.target.value })}
                    placeholder="sk-..."
                    style={{
                      width: "100%",
                      background: "var(--bg)",
                      border: "1px solid var(--border)",
                      borderRadius: "8px",
                      padding: "8px 12px",
                      paddingRight: "40px",
                      fontSize: "14px",
                      outline: "none",
                      transition: "all 0.2s ease"
                    }}
                    onFocus={(e) => {
                      e.target.style.borderColor = "var(--accent)";
                      e.target.style.boxShadow = "0 0 0 3px var(--accent-soft)";
                    }}
                    onBlur={(e) => {
                      e.target.style.borderColor = "var(--border)";
                      e.target.style.boxShadow = "none";
                    }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                      position: "absolute",
                      right: "8px",
                      top: "50%",
                      transform: "translateY(-50%)",
                      background: "none",
                      border: "none",
                      cursor: "pointer",
                      padding: "4px",
                      color: "var(--text-secondary)"
                    }}
                  >
                    {showPassword ? "🙈" : "👁️"}
                  </button>
                </div>
              </label>

              <label style={{ display: "block" }}>
                <span style={{ display: "block", marginBottom: "8px", fontWeight: "500" }}>
                  {t("admin.llm.model")}
                </span>
                <input
                  type="text"
                  value={config.model}
                  onChange={(e) => setConfig({ ...config, model: e.target.value })}
                  placeholder={selectedPreset?.defaultModel}
                  style={{
                    width: "100%",
                    background: "var(--bg)",
                    border: "1px solid var(--border)",
                    borderRadius: "8px",
                    padding: "8px 12px",
                    fontSize: "14px",
                    outline: "none",
                    transition: "all 0.2s ease"
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = "var(--accent)";
                    e.target.style.boxShadow = "0 0 0 3px var(--accent-soft)";
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = "var(--border)";
                    e.target.style.boxShadow = "none";
                  }}
                />
                {selectedPreset && (
                  <div style={{ marginTop: "8px", fontSize: "12px", color: "var(--text-secondary)" }}>
                    热门模型: {selectedPreset.popularModels.join(", ")}
                  </div>
                )}
              </label>
            </div>
          </div>

          {/* 高级设置 */}
          <div style={{
            border: "1px solid var(--border)",
            borderRadius: "8px",
            overflow: "hidden",
            marginBottom: "20px"
          }}>
            <button
              onClick={() => setShowAdvanced(!showAdvanced)}
              style={{
                width: "100%",
                background: "var(--bg)",
                border: "none",
                padding: "12px 16px",
                cursor: "pointer",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                fontSize: "14px",
                fontWeight: "500"
              }}
            >
              <span>{t("admin.llm.advancedSettings")}</span>
              <span>{showAdvanced ? "▲" : "▼"}</span>
            </button>

            {showAdvanced && (
              <div style={{ padding: "16px", borderTop: "1px solid var(--border)" }}>
                <div style={{ display: "grid", gap: "16px" }}>
                  {/* Temperature */}
                  <div>
                    <label style={{ display: "block", marginBottom: "8px", fontWeight: "500" }}>
                      {t("admin.llm.temperature")}: {config.temperature}
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="2"
                      step="0.1"
                      value={config.temperature}
                      onChange={(e) => setConfig({ ...config, temperature: parseFloat(e.target.value) })}
                      style={{
                        width: "100%",
                        height: "8px",
                        borderRadius: "4px",
                        background: "var(--border)",
                        outline: "none",
                        accentColor: "var(--accent)"
                      }}
                    />
                    <div style={{
                      display: "flex",
                      justifyContent: "space-between",
                      fontSize: "12px",
                      color: "var(--text-secondary)",
                      marginTop: "4px"
                    }}>
                      <span>0</span>
                      <span>1</span>
                      <span>2</span>
                    </div>
                  </div>

                  {/* Max Tokens */}
                  <div>
                    <label style={{ display: "block", marginBottom: "8px", fontWeight: "500" }}>
                      {t("admin.llm.maxTokens")}
                    </label>
                    <input
                      type="number"
                      value={config.max_tokens}
                      onChange={(e) => setConfig({ ...config, max_tokens: parseInt(e.target.value) || 4096 })}
                      min="1"
                      max="128000"
                      style={{
                        width: "100%",
                        background: "var(--bg)",
                        border: "1px solid var(--border)",
                        borderRadius: "8px",
                        padding: "8px 12px",
                        fontSize: "14px",
                        outline: "none"
                      }}
                    />
                  </div>

                  {/* Top P */}
                  <div>
                    <label style={{ display: "block", marginBottom: "8px", fontWeight: "500" }}>
                      {t("admin.llm.topP")}: {config.top_p}
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.05"
                      value={config.top_p}
                      onChange={(e) => setConfig({ ...config, top_p: parseFloat(e.target.value) })}
                      style={{
                        width: "100%",
                        height: "8px",
                        borderRadius: "4px",
                        background: "var(--border)",
                        outline: "none",
                        accentColor: "var(--accent)"
                      }}
                    />
                    <div style={{
                      display: "flex",
                      justifyContent: "space-between",
                      fontSize: "12px",
                      color: "var(--text-secondary)",
                      marginTop: "4px"
                    }}>
                      <span>0</span>
                      <span>0.5</span>
                      <span>1</span>
                    </div>
                  </div>

                  {/* Auth Mode */}
                  <div>
                    <label style={{ display: "block", marginBottom: "8px", fontWeight: "500" }}>
                      {t("admin.llm.authMode")}
                    </label>
                    <div style={{ display: "flex", gap: "16px" }}>
                      <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer" }}>
                        <input
                          type="radio"
                          name="authMode"
                          value="api_key"
                          checked={config.auth_mode === "api_key"}
                          onChange={(e) => setConfig({ ...config, auth_mode: e.target.value as "api_key" | "auth_token" })}
                          style={{ accentColor: "var(--accent)" }}
                        />
                        <span>{t("admin.llm.apiKeyMode")}</span>
                      </label>
                      <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer" }}>
                        <input
                          type="radio"
                          name="authMode"
                          value="auth_token"
                          checked={config.auth_mode === "auth_token"}
                          onChange={(e) => setConfig({ ...config, auth_mode: e.target.value as "api_key" | "auth_token" })}
                          style={{ accentColor: "var(--accent)" }}
                        />
                        <span>{t("admin.llm.authTokenMode")}</span>
                      </label>
                    </div>
                  </div>

                  {/* Custom Headers */}
                  <div>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                      <label style={{ fontWeight: "500" }}>{t("admin.llm.customHeaders")}</label>
                      <button
                        onClick={addHeader}
                        style={{
                          background: "transparent",
                          border: "1px solid var(--border)",
                          borderRadius: "6px",
                          padding: "4px 8px",
                          cursor: "pointer",
                          fontSize: "12px"
                        }}
                      >
                        + {t("admin.llm.addHeader")}
                      </button>
                    </div>
                    
                    {Object.keys(headersRef.current).length > 0 ? (
                      <div style={{ border: "1px solid var(--border)", borderRadius: "8px", overflow: "hidden" }}>
                        {Object.entries(headersRef.current).map(([key, value]) => (
                          <div
                            key={key}
                            style={{
                              display: "flex",
                              alignItems: "center",
                              gap: "12px",
                              padding: "8px 12px",
                              borderBottom: "1px solid var(--border)",
                              background: "var(--bg)"
                            }}
                          >
                            <code style={{ flex: 1, fontSize: "13px", background: "var(--bg-elevated)", padding: "4px 8px", borderRadius: "4px" }}>
                              {key}
                            </code>
                            <code style={{ flex: 2, fontSize: "13px", background: "var(--bg-elevated)", padding: "4px 8px", borderRadius: "4px" }}>
                              {value}
                            </code>
                            <button
                              onClick={() => removeHeader(key)}
                              style={{
                                background: "transparent",
                                border: "none",
                                cursor: "pointer",
                                color: "var(--danger)",
                                padding: "4px",
                                fontSize: "16px",
                                lineHeight: 1
                              }}
                            >
                              ×
                            </button>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div style={{
                        padding: "12px",
                        background: "var(--bg)",
                        border: "1px dashed var(--border)",
                        borderRadius: "8px",
                        textAlign: "center",
                        color: "var(--text-secondary)",
                        fontSize: "13px"
                      }}>
                        暂无自定义请求头
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* 当前激活模型切换区 */}
          {isConfigured && (
            <div style={{
              background: "var(--bg)",
              border: "1px solid var(--border)",
              borderRadius: "8px",
              padding: "16px"
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                <h3 style={{ margin: 0, fontSize: "14px", fontWeight: "600" }}>
                  {t("admin.llm.activeModel")}
                </h3>
                {isActiveProvider(selectedProvider) ? (
                  <span style={{
                    fontSize: "12px",
                    color: "var(--success)",
                    fontWeight: "500",
                    background: "var(--success-soft)",
                    padding: "4px 8px",
                    borderRadius: "4px"
                  }}>
                    {t("admin.llm.active")}
                  </span>
                ) : (
                  <button
                    onClick={setActiveModel}
                    style={{
                      background: "transparent",
                      border: "1px solid var(--accent)",
                      borderRadius: "6px",
                      padding: "4px 12px",
                      cursor: "pointer",
                      fontSize: "12px",
                      color: "var(--accent)"
                    }}
                  >
                    {t("admin.llm.switchModel")}
                  </button>
                )}
              </div>
              
              <div style={{ fontSize: "13px", color: "var(--text-secondary)" }}>
                {isActiveProvider(selectedProvider) ? (
                  <span>当前使用 {selectedPreset?.name} 的 {config.model || selectedPreset?.defaultModel}</span>
                ) : (
                  <span>{t("admin.llm.noActiveModel")}</span>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* 删除确认弹窗 */}
      {showDeleteConfirm && (
        <div style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: "rgba(0,0,0,0.5)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 1000
        }}>
          <div style={{
            background: "var(--bg-elevated)",
            borderRadius: "12px",
            padding: "24px",
            maxWidth: "400px",
            width: "90%",
            boxShadow: "0 4px 6px rgba(0,0,0,0.1)"
          }}>
            <h3 style={{ margin: "0 0 16px 0", fontSize: "18px" }}>{t("admin.llm.delete")}</h3>
            <p style={{ margin: "0 0 24px 0", color: "var(--text-secondary)" }}>
              {t("admin.llm.confirmDelete")}
            </p>
            <div style={{ display: "flex", justifyContent: "flex-end", gap: "12px" }}>
              <button
                onClick={() => setShowDeleteConfirm(false)}
                style={{
                  background: "transparent",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  padding: "8px 16px",
                  cursor: "pointer"
                }}
              >
                取消
              </button>
              <button
                onClick={deleteProvider}
                style={{
                  background: "var(--danger)",
                  color: "white",
                  border: "none",
                  borderRadius: "8px",
                  padding: "8px 16px",
                  cursor: "pointer",
                  fontWeight: "500"
                }}
                disabled={deleting}
              >
                {deleting ? "删除中..." : "确认删除"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
