import React, { useState, useRef } from "react";
import {
  View,
  Text,
  Button,
  Image,
  StyleSheet,
  ScrollView
} from "react-native";
import * as ImagePicker from "expo-image-picker";

export default function App() {
  const [frame, setFrame] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const [status, setStatus] = useState("Disconnected");

  const wsRef = useRef<WebSocket | null>(null);

  // 🔥 CHANGE THIS TO YOUR REAL IP
  const SERVER_HTTP = "http://192.168.12.110";
  const SERVER_WS = "ws://192.168.1.100:5000/ws";

  // =========================
  // 📸 PICK IMAGE + SCAN
  // =========================
  const pickImage = async () => {
    let resultPicker = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 1,
      base64: false
    });

    if (!resultPicker.canceled) {
      const uri = resultPicker.assets[0].uri;

      const formData = new FormData();
      formData.append("image", {
        uri,
        name: "photo.jpg",
        type: "image/jpeg"
      } as any);

      const res = await fetch(`${SERVER_HTTP}/scan`, {
        method: "POST",
        headers: {
          Authorization: "XR2-AUTH-TOKEN"
        },
        body: formData
      });

      const data = await res.json();
      setResult(data);
    }
  };

  // =========================
  // 🔴 LIVE STREAM (WS)
  // =========================
  const connectStream = () => {
    const ws = new WebSocket(SERVER_WS);
    wsRef.current = ws;

    ws.onopen = () => setStatus("Connected");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.frame) {
        setFrame("data:image/jpeg;base64," + data.frame);
      }

      if (data.detections) {
        setResult(data.detections);
      }
    };

    ws.onerror = () => setStatus("Error");
    ws.onclose = () => setStatus("Disconnected");
  };

  // =========================
  // ❌ DISCONNECT
  // =========================
  const disconnect = () => {
    wsRef.current?.close();
    setStatus("Disconnected");
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>XR2 MAX Vision System</Text>

      <Text style={styles.status}>Status: {status}</Text>

      {/* 🔥 ACTIONS */}
      <Button title="📸 Scan Image" onPress={pickImage} />
      <View style={{ height: 10 }} />
      <Button title="🔴 Start Live Vision" onPress={connectStream} />
      <View style={{ height: 10 }} />
      <Button title="❌ Stop Stream" onPress={disconnect} />

      {/* 🖼 LIVE FRAME */}
      {frame && (
        <Image source={{ uri: frame }} style={styles.image} />
      )}

      {/* 📊 RESULTS */}
      {result && (
        <View style={styles.resultBox}>
          <Text style={styles.resultTitle}>Detection Results:</Text>
          <Text style={styles.resultText}>
            {JSON.stringify(result, null, 2)}
          </Text>
        </View>
      )}
    </ScrollView>
  );
}

// =========================
// 🎨 STYLES
// =========================
const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#0a0a0a"
  },
  title: {
    fontSize: 26,
    fontWeight: "bold",
    color: "#00ffcc",
    marginBottom: 10
  },
  status: {
    color: "#fff",
    marginBottom: 15
  },
  image: {
    width: "100%",
    height: 300,
    marginTop: 20,
    borderRadius: 10
  },
  resultBox: {
    marginTop: 20,
    padding: 10,
    backgroundColor: "#111",
    borderRadius: 10
  },
  resultTitle: {
    color: "#00ffcc",
    fontWeight: "bold"
  },
  resultText: {
    color: "#fff",
    fontSize: 12
  }
});
