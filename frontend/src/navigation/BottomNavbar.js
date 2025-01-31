import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createStackNavigator } from "@react-navigation/stack";
import { Image, TouchableOpacity } from "react-native";
import Ionicons from "react-native-vector-icons/Ionicons";
import HomeScreen from "../screens/HomeScreen";
import AccountScreen from "../screens/AccountScreen";
import MenuScreen from "../screens/MenuScreen";
import CheckoutScreen from "../screens/CheckoutScreen";

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

const BottomNavbar = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === "Home") {
            iconName = focused ? "home" : "home-outline";
          } else if (route.name === "Account") {
            iconName = focused ? "person" : "person-outline";
          } else if (route.name === "Checkout") {
            iconName = focused ? "cart" : "cart-outline";
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: "#25A7FF",
        tabBarInactiveTintColor: "gray",
      })}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{ headerShown: false }}
      />
      <Tab.Screen
        name="Checkout"
        component={CheckoutScreen}
        options={{ headerShown: false }}
      />
      <Tab.Screen
        name="Account"
        component={AccountScreen}
        options={{ title: "Account" }}
      />
    </Tab.Navigator>
  );
};

function StackNavigator() {
  return (
    <Stack.Navigator>
      <Stack.Screen
        name="Main"
        component={BottomNavbar}
        options={{
          headerShown: true,
          headerStyle: {
            backgroundColor: "#25A7FF",
            elevation: 0,
            shadowOpacity: 0,
          },
          headerTitle: () => null,
          headerLeft: () => (
            <Image
              source={require("../../assets/images/logo.png")}
              style={{ width: 40, height: 40, marginLeft: 15 }}
              resizeMode="contain"
            />
          ),
          headerTitleAlign: "center",
          headerTintColor: "#fff",
          headerTransparent: false,
        }}
      />
      <Stack.Screen
        name="MenuScreen"
        component={MenuScreen}
        options={({ navigation }) => ({
          headerShown: true,
          headerStyle: {
            backgroundColor: "#25A7FF",
            elevation: 0,
            shadowOpacity: 0,
          },
          headerTitle: () => null,
          headerLeft: () => (
            <TouchableOpacity onPress={() => navigation.goBack()}>
              <Ionicons name="arrow-back" size={24} color="#fff" style={{ marginLeft: 15 }} />
            </TouchableOpacity>
          ),
          headerRight: () => (
            <Image
              source={require("../../assets/images/logo.png")}
              style={{ width: 40, height: 40, marginRight: 15 }}
              resizeMode="contain"
            />
          ),
          headerTitleAlign: "center",
          headerTintColor: "#fff",
          headerTransparent: false,
        })}
      />
      <Stack.Screen
        name="CheckoutScreen"
        component={CheckoutScreen}
        options={({ navigation }) => ({
          headerShown: true,
          headerStyle: {
            backgroundColor: "#25A7FF",
            elevation: 0,
            shadowOpacity: 0,
          },
          headerTitle: () => null,
          headerLeft: () => (
            <TouchableOpacity onPress={() => navigation.goBack()}>
              <Ionicons name="arrow-back" size={24} color="#fff" style={{ marginLeft: 15 }} />
            </TouchableOpacity>
          ),
          headerRight: () => (
            <Ionicons name="cart" size={24} color="#fff" style={{ marginRight: 15 }} />
          ),
          headerTitleAlign: "center",
          headerTintColor: "#fff",
          headerTransparent: false,
        })}
      />
    </Stack.Navigator>
  );
}

export default StackNavigator;