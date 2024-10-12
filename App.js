import { Camera, CameraType } from 'expo-camera/legacy';
import { useState } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View, Image } from 'react-native';

export default function App() {
  const [type, setType] = useState(CameraType.back);
  const [permission, requestPermission] = Camera.useCameraPermissions();
  const [camera, setCamera] = useState(null);
  const [processedImage, setProcessedImage] = useState()

  if (!permission) {
    return <View />;
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={{ textAlign: 'center' }}>We need your permission to show the camera</Text>
        <Button onPress={requestPermission} title="Grant Permission" />
      </View>
    );
  }

  function toggleCameraType() {
    setType(current => (current === CameraType.back ? CameraType.front : CameraType.back));
  }

  const snap = async () => {
    if (camera) {
      try {
        const photo = await camera.takePictureAsync({ base64: true });

        // Send the captured image data to the Flask server
        const response = await fetch('http://192.168.2.9:3000/process_image', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ image: photo.base64 }),
        });

        // Handle response from the server (optional)
        const data = await response.json();
        console.log('Server response:', data.message);
        setProcessedImage(data.processed_image)

        alert('Photo taken and sent to server!');
      } catch (error) {
        console.error('Error taking photo:', error);
        alert('Failed to take photo. Please try again.');
      }
    }
  };

  return (
    <View style={styles.container}>
      {processedImage && (
        <Image
          source={{ uri: `data:image/jpeg;base64,${processedImage}` }}
          style={{ width: 200, height: 200 }}
        />
      )}
      <Camera style={styles.camera} type={type} ref={ref => setCamera(ref)}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.button} onPress={toggleCameraType}>
            <Text style={styles.text}>Flip Camera</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={snap}>
            <Text style={styles.text}>Take Picture</Text>
          </TouchableOpacity>
        </View>
      </Camera>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: 'transparent',
    margin: 20,
  },
  button: {
    flex: 1,
    alignSelf: 'flex-end',
    alignItems: 'center',
    marginBottom: 100
  },
  text: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
});