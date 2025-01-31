import React, { createContext, useContext, useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";

const CheckoutCartContext = createContext();

export const CheckoutCartProvider = ({ children }) => {
  const [cart, setCart] = useState({});

  useEffect(() => {
    const loadCart = async () => {
      try {
        const storedCart = await AsyncStorage.getItem("cart");
        if (storedCart) {
          setCart(JSON.parse(storedCart));
        }
      } catch (error) {
        console.error("Failed to load cart from AsyncStorage:", error);
      }
    };
    loadCart();
  }, []);

  useEffect(() => {
    const saveCart = async () => {
      try {
        await AsyncStorage.setItem("cart", JSON.stringify(cart));
      } catch (error) {
        console.error("Failed to save cart to AsyncStorage:", error);
      }
    };
    saveCart();
  }, [cart]);

  const addToCart = (itemId, amount, itemDetails) => {
    setCart((prevCart) => ({
      ...prevCart,
      [itemId]: { amount, ...itemDetails },
    }));
  };

  const removeFromCart = (itemId) => {
    setCart((prevCart) => {
      const updatedCart = { ...prevCart };
      delete updatedCart[itemId];
      return updatedCart;
    });
  };

  const clearCart = () => {
    setCart({});
  };

  return (
    <CheckoutCartContext.Provider
      value={{ cart, addToCart, removeFromCart, clearCart }}
    >
      {children}
    </CheckoutCartContext.Provider>
  );
};

export const useCheckoutCart = () => useContext(CheckoutCartContext);