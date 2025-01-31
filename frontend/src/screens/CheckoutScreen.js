import React, { useState } from "react";
import { View, Text, TextInput, StyleSheet, FlatList, TouchableOpacity, Alert, ScrollView } from "react-native";
import Icon from "react-native-vector-icons/MaterialIcons";
import { useCheckoutCart } from "../context/CheckoutCartContext";

const CheckoutScreen = () => {
  const { cart, removeFromCart, clearCart } = useCheckoutCart();

  const [name, setName] = useState("");
  const [address, setAddress] = useState("");
  const [phone, setPhone] = useState("");

  const handlePlaceOrder = () => {
    if (!name || !address || !phone) {
      Alert.alert("Missing Information", "Please fill in all delivery details.");
      return;
    }
    Alert.alert("Order Placed", `Your order has been placed successfully!\n\nName: ${name}\nAddress: ${address}\nPhone: ${phone}`);
    clearCart();
    setName("");
    setAddress("");
    setPhone("");
  };

  const renderCartItem = ({ item }) => (
    <View style={styles.cartItemContainer}>
      <Text style={styles.cartItemName}>{item.name}</Text>
      <Text style={styles.cartItemAmount}>Amount: {item.amount}</Text>
      <Text style={styles.cartItemPrice}>£{(item.price * item.amount).toFixed(2)}</Text>
      <TouchableOpacity onPress={() => removeFromCart(item.id)}>
        <Icon name="delete" size={24} color="red" />
      </TouchableOpacity>
    </View>
  );

  const cartItems = Object.values(cart);
  const totalPrice = cartItems.reduce((total, item) => total + item.price * item.amount, 0);

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Checkout</Text>
      <FlatList
        data={cartItems}
        renderItem={renderCartItem}
        keyExtractor={(item) => item.id}
        scrollEnabled={false}
      />
      <Text style={styles.totalPrice}>Total: £{totalPrice.toFixed(2)}</Text>

      <TextInput
        style={styles.input}
        placeholder="Recipient Name"
        value={name}
        onChangeText={setName}
      />
      <TextInput
        style={styles.input}
        placeholder="Delivery Address"
        value={address}
        onChangeText={setAddress}
      />
      <TextInput
        style={styles.input}
        placeholder="Phone Number"
        value={phone}
        onChangeText={setPhone}
        keyboardType="phone-pad"
      />

      <TouchableOpacity style={styles.clearButton} onPress={clearCart}>
        <Text style={styles.clearButtonText}>Clear Cart</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.checkoutButton} onPress={handlePlaceOrder}>
        <Text style={styles.checkoutButtonText}>Place Order</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 16,
  },
  cartItemContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 8,
    borderBottomWidth: 1,
    borderBottomColor: "#ccc",
  },
  cartItemName: {
    fontSize: 16,
  },
  cartItemAmount: {
    fontSize: 14,
    color: "#666",
  },
  cartItemPrice: {
    fontSize: 14,
    fontWeight: "bold",
  },
  totalPrice: {
    fontSize: 18,
    fontWeight: "bold",
    marginTop: 16,
    textAlign: "right",
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    padding: 10,
    fontSize: 16,
    marginTop: 10,
  },
  clearButton: {
    backgroundColor: "red",
    padding: 12,
    borderRadius: 8,
    alignItems: "center",
    marginTop: 16,
  },
  clearButtonText: {
    color: "white",
    fontSize: 16,
    fontWeight: "bold",
  },
  checkoutButton: {
    backgroundColor: "green",
    padding: 12,
    borderRadius: 8,
    alignItems: "center",
    marginTop: 16,
  },
  checkoutButtonText: {
    color: "white",
    fontSize: 16,
    fontWeight: "bold",
  },
});

export default CheckoutScreen;