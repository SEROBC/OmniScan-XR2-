import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  Image,
  Button,
  StyleSheet,
  TextInput
} from "react-native";
import React, { useEffect, useState } from "react";
import { View, Text, Button, Image } from "react-native";
import React, { useState } from "react";

export default function App() {
  const [result, setResult] = useState(null);

  const uploadImage = async (e: any) => {
    const file = e.target.files[0];

    const formData = new FormData();
    formData.append("image", file);

    const res = await fetch("http://127.0.0.1:5000/scan", {
      method: "POST",
      headers: {
        Authorization: "XR2-AUTH-TOKEN"
      },
      body: formData
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>XR2 Detection System</h1>

      <input type="file" onChange={uploadImage} />

      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

export default function App() {
  const [frame, setFrame] = useState<string | null>(null);
  const [connected, setConnected] = useState(false);
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
