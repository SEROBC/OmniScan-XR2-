import React, { useEffect, useState } from "react";
import { View, Image } from "react-native";

export default function App() {
  const [frame, setFrame] = useState<string | null>(null);

  useEffect(() => {
    const ws = new WebSocket("ws://192.168.1.100:5000/ws/stream");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setFrame("data:image/jpeg;base64," + data.frame);
    };

    return () => ws.close();
  }, []);

  return (
    <View style={{ flex: 1 }}>
      {frame && (
        <Image
          source={{ uri: frame }}
          style={{ width: "100%", height: "100%" }}
        />
      )}
    </View>
  );
}
