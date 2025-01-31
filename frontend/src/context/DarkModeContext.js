import React, { createContext, useState, useEffect, useContext } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useColorScheme } from "react-native";
import colors from "../../colors";

const DarkModeContext = createContext();

export const useDarkMode = () => useContext(DarkModeContext);

export const DarkModeProvider = ({ children }) => {
    const systemTheme = useColorScheme()
    const [isDarkMode, setIsDarkMode] = useState(systemTheme === 'dark');
    const [useSystemTheme, setUseSystemTheme] = useState(true);

    useEffect(() => {
        const loadPreference = async () => {
            const storeMode = await AsyncStorage.getItem('darkMode');
            const storedSystemThemePreference = await AsyncStorage.getItem('useSystemTheme');

            if (storedSystemThemePreference !== null) {
                setUseSystemTheme(storedSystemThemePreference === 'true');
            }

            if (storeMode !== null && storedSystemThemePreference === 'false') {
                setIsDarkMode(storeMode === 'true');
            } else {
                setIsDarkMode(systemTheme === 'dark');
            }
        };
        loadPreference();
    }, [systemTheme])

    const toggleDarkMode = async () => {
        if (useSystemTheme) {
            setUseSystemTheme(false);
            await AsyncStorage.setItem('useSystemTheme', JSON.stringify(false));
        }

        const newMode = !isDarkMode;
        setIsDarkMode(newMode);
        await AsyncStorage.setItem('darkMode', JSON.stringify(newMode));
    };

    const toggleSystemTheme = async () => {
        const newUseSystemTheme = !useSystemTheme;
        setUseSystemTheme(newUseSystemTheme);

        await AsyncStorage.setItem('useSystemTheme', JSON.stringify(newUseSystemTheme));
        if (newUseSystemTheme) {
            setIsDarkMode(systemTheme === 'dark');
        }
    };

    const themeColors = {
        text: isDarkMode ? colors.textLight: colors.textDark,
        background: isDarkMode ? colors.backgroundLight : colors.backgroundDark,
        primary: isDarkMode ? colors.primaryLight : colors.primaryDark,
        secondary: isDarkMode ? colors.secondaryLight : colors.secondaryDark,
        accent: isDarkMode ? colors.accentLight : colors.accentDark,
        surface: isDarkMode ? colors.surfaceLight : colors.surfaceDark
    };

    return (
        <DarkModeContext.Provider value={{ isDarkMode, toggleDarkMode, themeColors, useSystemTheme, toggleSystemTheme }}>
            {children}
        </DarkModeContext.Provider>
    )
}