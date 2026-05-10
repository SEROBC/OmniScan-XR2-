import React, { useEffect, useState } from "react";
import { View, Text, Button, Image } from "react-native";

export default function App() {
  const [frame, setFrame] = useState<string | null>(null);
  const [connected, setConnected] = useState(false);

  const connect = () => {
    const ws = new WebSocket("ws://192.168.1.100:5000/ws");

    ws.onopen = () => setConnected(true);

    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      setFrame(`data:image/jpeg;base64,${data.frame}`);
    };
  };

  return (
    <View style={{ padding: 20 }}>
      <Text>XR2 MAX+</Text>
      <Text>Status: {connected ? "ONLINE" : "OFFLINE"}</Text>

      <Button title="Start Vision" onPress={connect} />

      {frame && (
        <Image
          source={{ uri: frame }}
          style={{ width: "100%", height: 400 }}
        />
      )}
    </View>
  );
}      <Button title="Connect Camera" onPress={connect} />

      {frame && (
        <Image source={{ uri: frame }} style={styles.image} />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: "bold" },
  image: { width: "100%", height: 400 }
});
