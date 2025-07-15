import * as React from "react";
import { Image } from "expo-image";
import { StyleSheet, View } from "react-native";
import Vector2 from "../assets/vector-2.svg";
import { Padding, Gap } from "../GlobalStyles";

interface FrameComponent11Props {
  selectedImageUri?: string;
}

const FrameComponent11: React.FC<FrameComponent11Props> = ({ selectedImageUri }) => {
  return (
    <View style={styles.images11Parent}>
      <View style={styles.imageContainer}>
        <Image
          style={[styles.images11, { borderWidth: 1, borderColor: 'white' }]}
          contentFit="cover"
          source={selectedImageUri ? { uri: selectedImageUri } : require("../assets/images-1-11.png")}
        />
        <View style={styles.vectorOverlay}>
          {/* 좌상단 */}
          <Vector2 style={{ position: 'absolute', top: -10, left: -10, width: 48, height: 48 }} />
          {/* 우상단 */}
          <Vector2 style={{ position: 'absolute', top: -10, right: -10, width: 48, height: 48, transform: [{ rotate: '90deg' }] }} />
          {/* 우하단 */}
          <Vector2 style={{ position: 'absolute', bottom: -10, right: -10, width: 48, height: 48, transform: [{ rotate: '180deg' }] }} />
          {/* 좌하단 */}
          <Vector2 style={{ position: 'absolute', bottom: -10, left: -10, width: 48, height: 48, transform: [{ rotate: '-90deg' }] }} />
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  images11: {
    width: 342,
    height: 321,
    zIndex: 0,
  },
  imageContainer: {
    position: "relative",
    width: 342,
    height: 321,
    alignItems: 'center',
    justifyContent: 'center',
    alignSelf: 'center',
    marginLeft: 'auto',
    marginRight: 'auto',
  },
  frameChild: {},
  vectorOverlay: {
    position: "absolute",
    top: 10,
    left: 10,
    right: 10,
    bottom: 10,
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
    alignItems: "flex-start",
    zIndex: 1,
  },
  images11Parent: {
    padding: 9,
    gap: Gap.gap_10,
    alignSelf: "stretch",
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: 'auto',
    marginRight: 'auto',
  },
});

export default FrameComponent11;
