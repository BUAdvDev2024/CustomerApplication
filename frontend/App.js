import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import StackNavigator from './src/navigation/BottomNavbar';
import { NavigationContainer } from '@react-navigation/native';
import { CheckoutCartProvider } from './src/context/CheckoutCartContext';

export default function App() {
  return (
    <CheckoutCartProvider>
      <NavigationContainer>
        <StackNavigator />
      </NavigationContainer>
    </CheckoutCartProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
