
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Bot, User } from "lucide-react";
import { cn } from "@/lib/utils";
import api from "@/services/api";

/* -----------------------------
   TYPES
----------------------------- */

interface Recommendation {
  module: string;
  problem: string;
  action: string;
  impact: string;
}

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  recommendations?: Recommendation[];
}

/* -----------------------------
   UNIQUE ID GENERATOR
----------------------------- */

const generateId = () =>
  `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;

/* -----------------------------
   COMPONENT
----------------------------- */

export default function AIRecommendation() {

  const [messages, setMessages] = useState<Message[]>([
    {
      id: generateId(),
      role: "assistant",
      content:
        "Hello! I'm your AI Sustainability Advisor. Ask me about emissions, AQI, or sustainability improvements.",
    },
  ]);

  const [input, setInput] = useState("");

  /* -----------------------------
     CALL DJANGO AI API
  ----------------------------- */

  const fetchAIRecommendations = async (query: string) => {

    try {

      const res = await api.post("/ai/recommendations/", {
        query: query,
      });

      return res.data.recommendations;

    } catch (error) {

      console.error("AI API Error:", error);

      return [
        {
          module: "System",
          problem: "Unable to fetch AI analysis",
          action: "Check backend server",
          impact: "No recommendations available",
        },
      ];

    }

  };

  /* -----------------------------
     HANDLE SEND
  ----------------------------- */

  const handleSend = async () => {

    if (!input.trim()) return;

    const userMessage: Message = {
      id: generateId(),
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);

    const question = input;

    setInput("");

    const recommendations = await fetchAIRecommendations(question);

    const aiMessage: Message = {
      id: generateId(),
      role: "assistant",
      content:
        "Based on your current sustainability data, here are my recommendations:",
      recommendations: recommendations,
    };

    setMessages((prev) => [...prev, aiMessage]);

  };

  return (
    <div className="flex h-[calc(100vh-8rem)] gap-4">

      {/* CHAT PANEL */}

      <div className="flex flex-1 flex-col rounded-xl border bg-card">

        {/* HEADER */}

        <div className="flex items-center gap-2 border-b px-4 py-3">

          <Bot className="h-5 w-5 text-primary" />

          <div>
            <p className="text-sm font-semibold">
              AI Sustainability Advisor
            </p>

            <p className="text-[10px] text-muted-foreground">
              Real-time sustainability analysis
            </p>
          </div>

        </div>

        {/* MESSAGES */}

        <div className="flex-1 space-y-4 overflow-y-auto p-4">

          {messages.map((msg) => (

            <div
              key={msg.id}
              className={cn(
                "flex gap-2.5",
                msg.role === "user" && "justify-end"
              )}
            >

              {msg.role === "assistant" && (

                <div className="flex h-7 w-7 items-center justify-center rounded-full bg-primary">
                  <Bot className="h-3.5 w-3.5 text-white" />
                </div>

              )}

              <div className="max-w-[75%] space-y-2">

                <div
                  className={cn(
                    "rounded-xl px-3 py-2 text-sm",
                    msg.role === "user"
                      ? "bg-primary text-white"
                      : "bg-muted"
                  )}
                >
                  {msg.content}
                </div>

                {msg.recommendations && (

                  <div className="grid gap-2 sm:grid-cols-2">

                    {msg.recommendations.map((rec, i) => (

                      <div
                        key={`${rec.module}-${i}`}
                        className="rounded-lg border-l-4 border-primary bg-muted p-3"
                      >

                        <p className="text-[10px] font-semibold uppercase text-muted-foreground">
                          {rec.module}
                        </p>

                        <p className="text-xs mt-1">
                          <strong>Problem:</strong> {rec.problem}
                        </p>

                        <p className="text-xs">
                          <strong>Action:</strong> {rec.action}
                        </p>

                        <p className="text-xs">
                          <strong>Impact:</strong> {rec.impact}
                        </p>

                      </div>

                    ))}

                  </div>

                )}

              </div>

              {msg.role === "user" && (

                <div className="flex h-7 w-7 items-center justify-center rounded-full bg-secondary">
                  <User className="h-3.5 w-3.5" />
                </div>

              )}

            </div>

          ))}

        </div>

        {/* INPUT */}

        <div className="border-t p-3">

          <div className="flex gap-2">

            <Input
              value={input}
              placeholder="Ask about sustainability improvements..."
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
            />

            <Button size="icon" onClick={handleSend}>
              <Send className="h-4 w-4" />
            </Button>

          </div>

        </div>

      </div>

    </div>
  );
}

