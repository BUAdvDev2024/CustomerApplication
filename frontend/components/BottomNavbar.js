import React from "react";
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';
import HomeScreen from '../screens/HomeScreen';
import AccountScreen from '../screens/AccountScreen';

const Tab = createBottomTabNavigator();

const BottomNavbar = () => {
    const { themeColors } = useDarkMode();
    return (
        <Tab.Navigator
            screenOptions={({ route }) => ({
                tabBarIcon: ({ focused, color, size }) => {
                    let iconName;

                    if (route.name === 'Home') {
                        iconName = focused ? 'home' : 'home-outline';
                    } else if (route.name === 'Account') {
                        iconName = focused ? 'person' : 'person-outline';
                    }

                    return <Ionicons name={iconName} size={size} color={color} />;
                },
            })}
        >
            <Tab.Screen
                name='Home'
                component={HomeScreen}
                options={{ title: 'Home'}}
            />
            <Tab.Screen
                name='Account'
                component={AccountScreen}
                options={{ title: 'Account'}}
            />
        </Tab.Navigator>
    );
};

export default BottomNavbar;