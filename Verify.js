import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';

const API = "http://127.0.0.1:8000";

function Verify({email}) {
  const webcamRef = useRef(null);
  const [message, setMessage] = useState("");

  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    const blob = await fetch(imageSrc).then(res => res.blob());
    const formData = new FormData();
    formData.append("email", email);
    formData.append("file", blob, "face.jpg");
    const res = await fetch(API + "/verify/face", {method:"POST", body: formData});
    const data = await res.json();
    setMessage(data.message);
  };

  return (
    <div>
      <h2>Biometric Verification</h2>
      <Webcam audio={false} ref={webcamRef} screenshotFormat="image/jpeg" />
      <br/>
      <button onClick={capture}>Verify Face</button>
      <p>{message}</p>
    </div>
  );
}

export default Verify;
