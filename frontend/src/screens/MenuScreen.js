import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  SectionList,
  Image,
  TouchableOpacity,
  Alert,
  TextInput,
} from "react-native";
import Icon from "react-native-vector-icons/MaterialIcons";
import { useCheckoutCart } from "../context/CheckoutCartContext";

const MenuScreen = ({ navigation }) => {
  const [menuItems, setMenuItems] = useState([]);
  const { cart, addToCart, removeFromCart } = useCheckoutCart();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://YOUR_DEVICE_IP_HERE/api/get_data");
        const data = await response.json();
        const flattenedItems = flattenMenuItems(data.restaurants);
        setMenuItems(flattenedItems);
      } catch (error) {
        Alert.alert("Error", "Failed to fetch menu data.");
        console.error(error);
      }
    };
    fetchData();
  }, []);

  const flattenMenuItems = (restaurants) => {
    const allItems = [];
    const uniqueIds = new Set();

    restaurants.forEach((restaurant) => {
      restaurant.menus.forEach((menu) => {
        menu.categories.forEach((category) => {
          category.items.forEach((item) => {
            if (!uniqueIds.has(item.id)) {
              uniqueIds.add(item.id);
              allItems.push({
                ...item,
                category: category.name,
              });
            }
          });
        });
      });
    });

    return allItems;
  };

  const groupItemsByCustomCategories = (items) => {
    const groupedItems = {
      Starters: [],
      Appetizers: [],
      Pizzas: [],
      Drinks: [],
    };

    items.forEach((item) => {
      if (item.category.toLowerCase().includes("starter")) {
        groupedItems.Starters.push(item);
      } else if (item.category.toLowerCase().includes("appetizer")) {
        groupedItems.Appetizers.push(item);
      } else if (item.category.toLowerCase().includes("pizza")) {
        groupedItems.Pizzas.push(item);
      } else if (item.category.toLowerCase().includes("drink")) {
        groupedItems.Drinks.push(item);
      }
    });

    return groupedItems;
  };

  const groupedItems = groupItemsByCustomCategories(menuItems);
  const sections = Object.keys(groupedItems).map((category) => ({
    title: category,
    data: groupedItems[category],
  }));

  const renderItem = ({ item }) => {
    const isInCart = cart.hasOwnProperty(item.id);
    const amount = isInCart ? cart[item.id].amount : 1;

    return (
      <View style={styles.itemContainer}>
        <Image
          source={{ uri: item.image || "https://picsum.photos/200" }}
          style={styles.itemImage}
        />
        <View style={styles.itemDetails}>
          <Text style={styles.itemName}>{item.name}</Text>
          <Text style={styles.itemPrice}>£{item.price.toFixed(2)}</Text>
          <Text style={styles.itemDietary}>
            {item.dietary.join(", ") || "No dietary info"}
          </Text>
        </View>
        <View style={styles.amountContainer}>
          <TextInput
            style={styles.amountInput}
            value={amount.toString()}
            onChangeText={(text) => {
              const newAmount = parseInt(text, 10) || 1;
              addToCart(item.id, newAmount, item);
            }}
            keyboardType="numeric"
          />
          <TouchableOpacity
            onPress={() => {
              if (isInCart) {
                removeFromCart(item.id);
              } else {
                addToCart(item.id, amount, item);
              }
            }}
          >
            <Icon
              name={isInCart ? "check-circle" : "add-circle"}
              size={24}
              color={isInCart ? "green" : "#25A7FF"}
            />
          </TouchableOpacity>
        </View>
        <Icon
          name="loyalty"
          size={20}
          color={item.rewardEligible ? "green" : "red"}
        />
      </View>
    );
  };

  const totalItems = Object.keys(cart).length;

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Pack your order!</Text>
      <SectionList
        sections={sections}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        renderSectionHeader={({ section: { title } }) => (
          <Text style={styles.sectionHeader}>{title}</Text>
        )}
        contentContainerStyle={styles.sectionListContent}
      />
      {totalItems > 0 && (
        <View style={styles.checkoutButtonContainer}>
          <TouchableOpacity
            style={styles.checkoutButton}
            onPress={() => navigation.navigate("CheckoutScreen")}
          >
            <Text style={styles.checkoutButtonText}>
              Checkout ({totalItems} items)
            </Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#25A7FF",
    paddingHorizontal: 5,
    paddingTop: 5,
  },
  header: {
    fontSize: 40,
    fontWeight: "bold",
    alignSelf: "center",
    marginBottom: 10,
    color: "white",
  },
  sectionListContent: {
    paddingBottom: 120,
  },
  sectionHeader: {
    backgroundColor: "#25A7FF",
    color: "white",
    fontSize: 16,
    fontWeight: "bold",
    paddingVertical: 8,
    paddingHorizontal: 10,
  },
  itemContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "white",
    padding: 8,
    marginVertical: 4,
    marginHorizontal: 10,
    borderRadius: 8,
  },
  itemImage: {
    width: 40,
    height: 40,
    borderRadius: 20,
    marginRight: 8,
  },
  itemDetails: {
    flex: 1,
  },
  itemName: {
    fontSize: 14,
    fontWeight: "bold",
  },
  itemPrice: {
    fontSize: 12,
    color: "#666",
  },
  itemDietary: {
    fontSize: 10,
    color: "#999",
  },
  amountContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginRight: 8,
  },
  amountInput: {
    width: 40,
    height: 24,
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 5,
    paddingHorizontal: 4,
    marginRight: 8,
    textAlign: "center",
    fontSize: 12,
  },
  checkoutButtonContainer: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: "#25A7FF",
    padding: 10,
    paddingBottom: 40,
    borderTopWidth: 1,
    borderTopColor: "#ccc",
  },
  checkoutButton: {
    backgroundColor: "white",
    padding: 15,
    borderRadius: 10,
    alignItems: "center",
  },
  checkoutButtonText: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#25A7FF",
  },
});

export default MenuScreen;