import React, { useEffect, useState } from "react";

export default function Dashboard() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    const ws = new WebSocket("ws://YOUR_SERVER/ws");

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      setData((prev) => [msg, ...prev.slice(0, 20)]);
    };
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>XR2 Command Center</h1>

      {data.map((d, i) => (
        <div key={i}>
          <p>Detections: {JSON.stringify(d.detections)}</p>
        </div>
      ))}
    </div>
  );
}
