import { useState } from "react";
import axios from "axios";

function App() {
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [translation, setTranslation] = useState("");
  const [targetLang, setTargetLang] = useState("fr");
  const [loading, setLoading] = useState(false);
  let mediaRecorder;

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    const chunks = [];
    mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunks, { type: "audio/wav" });
      const formData = new FormData();
      formData.append("file", blob, "recording.wav");
      formData.append("target_lang", targetLang);
      setLoading(true);
      const res = await axios.post("http://localhost:8000/translate", formData);
      setTranscript(res.data.original_text);
      setTranslation(res.data.translated_text);
      setLoading(false);
    };
    mediaRecorder.start();
    setRecording(true);
    setTimeout(() => { mediaRecorder.stop(); setRecording(false); }, 5000);
  };

  return (
    <div style={{ padding: 40, fontFamily: "Arial", maxWidth: 600, margin: "0 auto" }}>
      <h1>🎙️ Speech Translator</h1>
      <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}
        style={{ padding: 10, fontSize: 16, marginBottom: 20 }}>
        <option value="fr">French</option>
        <option value="es">Spanish</option>
        <option value="de">German</option>
        <option value="hi">Hindi</option>
      </select>
      <br />
      <button onClick={startRecording} disabled={recording || loading}
        style={{ padding: "15px 30px", fontSize: 18, background: recording ? "red" : "green",
          color: "white", border: "none", borderRadius: 10, cursor: "pointer" }}>
        {recording ? "🔴 Recording..." : loading ? "⏳ Processing..." : "🎙️ Start Speaking (5 sec)"}
      </button>
      {transcript && <div style={{ marginTop: 30, padding: 20, background: "#f0f0f0", borderRadius: 10 }}>
        <h3>Original:</h3><p>{transcript}</p>
        <h3>Translated:</h3><p>{translation}</p>
      </div>}
    </div>
  );
}

export default App;