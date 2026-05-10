import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  Image,
  Button,
  StyleSheet,
  TextInput
} from "react-native";

export default function App() {
  const [frame, setFrame] = useState<string | null>(null);
  const [token, setToken] = useState("");
  const [status, setStatus] = useState("Disconnected");

  const SERVER = "ws://192.168.1.100:5000/ws";

  const connect = () => {
    const ws = new WebSocket(SERVER);

    ws.onopen = () => setStatus("Connected");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setFrame("data:image/jpeg;base64," + data.frame);
    };

    ws.onerror = () => setStatus("Error");
    ws.onclose = () => setStatus("Closed");
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>XR2 Vision System</Text>
      <Text>Status: {status}</Text>

      <Button title="Connect Camera" onPress={connect} />

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
