import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  SafeAreaView,
  Image,
  TouchableOpacity,
  TextInput,
  TouchableHighlight,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';
import * as Location from 'expo-location';
import { useNavigation } from '@react-navigation/native';

const HomeScreen = () => {
  const [selectedOption, setSelectedOption] = useState('Deliver');
  const [postcode, setPostcode] = useState('');
  const [location, setLocation] = useState(null);
  const navigation = useNavigation();

  const getCurrentLocation = async () => {
    let { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission Denied', 'Allow the app to use location services.');
      return;
    }

    let location = await Location.getCurrentPositionAsync({});
    setLocation(location);
    Alert.alert('Location Found', `Latitude: ${location.coords.latitude}, Longitude: ${location.coords.longitude}`);
  };

  return (
    <SafeAreaView style={styles.container}>
      <Image source={require('../../assets/images/pizza.png')} style={styles.image} />

      <Text style={styles.header}>START YOUR ORDER</Text>

      <View style={styles.toggleContainer}>
        <TouchableOpacity
          style={[
            styles.toggleOption,
            selectedOption === 'Deliver' && styles.selectedOption,
          ]}
          onPress={() => setSelectedOption('Deliver')}
        >
          <Icon name="truck" size={20} color={selectedOption === 'Deliver' ? 'white' : '#25A7FF'} />
          <Text style={[styles.toggleText, selectedOption === 'Deliver' && styles.selectedText]}>
            Deliver
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[
            styles.toggleOption,
            selectedOption === 'Collect' && styles.selectedOption,
          ]}
          onPress={() => setSelectedOption('Collect')}
        >
          <Icon name="map-pin" size={20} color={selectedOption === 'Collect' ? 'white' : '#25A7FF'} />
          <Text style={[styles.toggleText, selectedOption === 'Collect' && styles.selectedText]}>
            Collect
          </Text>
        </TouchableOpacity>
      </View>

      <View style={styles.contentContainer}>
        {selectedOption === 'Deliver' ? (
          <>
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.input}
                placeholder="Delivery postcode"
                value={postcode}
                onChangeText={setPostcode}
              />
              <TouchableOpacity style={styles.button} onPress={() => navigation.navigate("MenuScreen")}>
                <Text style={styles.buttonText}>View Menu</Text>
              </TouchableOpacity>
            </View>
            <Text style={styles.exampleText}>for example, BH12 5BB</Text>

            <View style={styles.locationButtonContainer}>
              <TouchableHighlight
                style={styles.locationButton}
                underlayColor="#ddd"
                onPress={getCurrentLocation}
              >
                <View style={styles.locationContainer}>
                  <Icon name="location-arrow" size={20} color="#25A7FF" />
                  <Text style={styles.locationText}>Use My Current Location</Text>
                </View>
              </TouchableHighlight>
            </View>
          </>
        ) : (
          <>
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.input}
                placeholder="Collect postcode"
                value={postcode}
                onChangeText={setPostcode}
              />
              <TouchableOpacity style={styles.button} onPress={() => navigation.navigate("MenuScreen")}>
                <Text style={styles.buttonText}>View Menu</Text>
              </TouchableOpacity>
            </View>
            <Text style={styles.exampleText}>for example, BH12 5BB</Text>

            <View style={styles.locationButtonContainer}>
              <TouchableHighlight
                style={styles.locationButton}
                underlayColor="#ddd"
                onPress={getCurrentLocation}
              >
                <View style={styles.locationContainer}>
                  <Icon name="location-arrow" size={20} color="#25A7FF" />
                  <Text style={styles.locationText}>Use My Current Location</Text>
                </View>
              </TouchableHighlight>
            </View>
          </>
        )}
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  image: {
    width: '100%',
    height: 250,
    resizeMode: 'cover',
    marginTop: 0,
  },
  header: {
    fontSize: 30,
    fontWeight: 'bold',
    color: '#25A7FF',
    textAlign: 'center',
    marginTop: 10,
  },
  toggleContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 20,
    marginHorizontal: 20,
    backgroundColor: '#fff',
    borderRadius: 25,
    padding: 10,
  },
  toggleOption: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 20,
  },
  selectedOption: {
    backgroundColor: '#25A7FF',
  },
  toggleText: {
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 10,
    color: '#25A7FF',
  },
  selectedText: {
    color: 'white',
  },
  contentContainer: {
    marginTop: 20,
    paddingHorizontal: 20,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    padding: 10,
    marginRight: 10,
  },
  button: {
    backgroundColor: '#25A7FF',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  exampleText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 20,
  },
  locationButtonContainer: {
    alignItems: 'center',
  },
  locationButton: {
    width: '70%',
    borderRadius: 15,
    backgroundColor: '#fff',
    padding: 10,
  },
  locationContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  locationText: {
    marginLeft: 10,
    color: '#25A7FF',
    fontWeight: 'bold',
  },
});

export default HomeScreen;