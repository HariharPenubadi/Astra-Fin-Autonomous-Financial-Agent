import { useState, useRef, useEffect } from "react";
import { Send, Cpu, Database, Bot, User } from "lucide-react";

export default function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hello! I am ASTRA. Ask me about your finances." }
  ]);
  const [brainState, setBrainState] = useState("Idle");
  const [memoryState, setMemoryState] = useState("No updates yet.");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async () => {
    if (!query.trim()) return;

    const newMsgs = [...messages, { role: "user", content: query }];
    setMessages(newMsgs);
    setQuery("");
    setLoading(true);
    setBrainState("Thinking...");

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantMsg = { role: "assistant", content: "" };

      setMessages((prev) => [...prev, assistantMsg]);

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const jsonStr = line.replace("data: ", "");
            try {
              const data = JSON.parse(jsonStr);

              if (data.type === "brain") {
                setBrainState(data.content);
              }
              else if (data.type === "memory") {
                setMemoryState(data.content);
              }
              else if (data.type === "response") {
                assistantMsg.content = data.content;
                setMessages((prev) => {
                  const updated = [...prev];
                  updated[updated.length - 1] = { ...assistantMsg };
                  return updated;
                });
              }
            } catch (e) {
              console.error("Parse error", e);
            }
          }
        }
      }
    } catch (error) {
      console.error("Fetch error", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen text-slate-200 font-sans">
      <div className="w-1/3 bg-slate-900 border-r border-slate-700 p-6 flex flex-col gap-6">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
          ASTRA FIN PRO
        </h1>

        <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-lg">
          <div className="flex items-center gap-2 mb-2 text-blue-400">
            <Cpu size={20} />
            <h2 className="font-semibold uppercase tracking-wider text-sm">Planner</h2>
          </div>
          <div className="font-mono text-lg text-white">
            {brainState}
          </div>
        </div>

        <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-lg">
          <div className="flex items-center gap-2 mb-2 text-emerald-400">
            <Database size={20} />
            <h2 className="font-semibold uppercase tracking-wider text-sm">Live Memory</h2>
          </div>
          <div className="font-mono text-sm text-slate-300 whitespace-pre-wrap">
            {memoryState}
          </div>
        </div>
      </div>

      <div className="w-2/3 bg-slate-950 flex flex-col">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-4 ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
              {msg.role === "assistant" && (
                <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center shrink-0">
                  <Bot size={18} />
                </div>
              )}

              <div className={`max-w-[80%] p-4 rounded-2xl whitespace-pre-wrap leading-relaxed ${
                msg.role === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-slate-800 text-slate-200 border border-slate-700 rounded-bl-none"
              }`}>
                {msg.content}
              </div>

              {msg.role === "user" && (
                <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center shrink-0">
                  <User size={18} />
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 bg-slate-900 border-t border-slate-800">
          <div className="max-w-4xl mx-auto relative flex items-center gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Ask about your investments..."
              disabled={loading}
              className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-4 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all placeholder:text-slate-500"
            />
            <button
              onClick={handleSend}
              disabled={loading || !query}
              className="absolute right-2 p-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send size={20} />
            </button>
          </div>
          <div className="text-center mt-2 text-xs text-slate-500">
            Powered by Fine-tuned LLaMA-3, LangGraph & React
          </div>
        </div>
      </div>
    </div>
  );
}