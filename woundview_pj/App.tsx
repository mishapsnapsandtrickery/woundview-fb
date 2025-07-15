const Stack = createNativeStackNavigator();
import * as React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { useFonts } from "expo-font";
import Intro from "./screens/Intro";
import Result from "./screens/Result";
import Component4 from "./screens/Component4";
import Timelinemain from "./screens/Timelinemain";
import Home from "./screens/Home";
import Checklist from "./screens/Checklist";
import PhotoOption from "./screens/PhotoOption";
import CameraScreen from "./screens/CameraScreen";
import UploadComplete from "./screens/UploadComplete";
import ImageUploader from "./screens/ImageUploader";
import Ailoading from "./screens/Ailoading";
import ImageEditor from "./screens/ImageEditor";
import Timelinerecord from "./screens/Timelinerecord";
import RecordEdit from "./screens/RecordEdit";
import Community from "./screens/Community";
import Mypage from "./screens/Mypage";
import MIcon from "react-native-vector-icons/MaterialCommunityIcons";
import { IconRegistry, ApplicationProvider } from "@ui-kitten/components";
import * as eva from "@eva-design/eva";

import { createNativeStackNavigator } from "@react-navigation/native-stack";
import {
  View,
  Text,
  Pressable,
  TouchableOpacity,
  StyleSheet,
} from "react-native";

const App = () => {
  const [hideSplashScreen, setHideSplashScreen] = React.useState(true);

  const [fontsLoaded, error] = useFonts({
    "Inter-Light": require("./assets/fonts/Inter-Light.ttf"),
    "Inter-Regular": require("./assets/fonts/Inter-Regular.ttf"),
    "Inter-Medium": require("./assets/fonts/Inter-Medium.ttf"),
    "Inter-SemiBold": require("./assets/fonts/Inter-SemiBold.ttf"),
    "Inter-Bold": require("./assets/fonts/Inter-Bold.ttf"),
    "Inter-ExtraBold": require("./assets/fonts/Inter-ExtraBold.ttf"),
  });

  function MaterialIcon({ name, style }: { name: string; style?: any }) {
    const { height, tintColor, ...iconStyle } = StyleSheet.flatten(style);
    if (typeof name !== 'string') return null;
    return (
      <MIcon name={name} size={height} color={tintColor} style={iconStyle} />
    );
  }

  const IconProvider = (name: string) => ({
    toReactElement: (props: any) => MaterialIcon({ name, ...props }),
  });

  function createIconsMap() {
    return new Proxy(
      {},
      {
        get(target, name) {
          if (typeof name === 'string') {
            return IconProvider(name);
          }
          // If name is a symbol, return a dummy icon provider or undefined
          return () => null;
        },
      },
    );
  }
  const MaterialIconsPack = {
    name: "material",
    icons: createIconsMap(),
  };

  if (!fontsLoaded && !error) {
    return null;
  }

  return (
    <>
      <IconRegistry icons={[MaterialIconsPack]} />
      <ApplicationProvider {...eva} theme={eva.light}>
        <NavigationContainer>
          {hideSplashScreen ? (
            <Stack.Navigator
              initialRouteName="Intro"
              screenOptions={{ headerShown: false }}
            >
              <Stack.Screen
                name="Intro"
                component={Intro}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="Result"
                component={Result}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="Component4"
                component={Component4}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="Timelinemain"
                component={Timelinemain}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="Home"
                component={Home}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="Checklist"
                component={Checklist}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="PhotoOption"
                component={PhotoOption}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="CameraScreen"
                component={CameraScreen}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="UploadComplete"
                component={UploadComplete}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="ImageUploader"
                component={ImageUploader}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="Ailoading"
                component={Ailoading}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="ImageEditor"
                component={ImageEditor}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="Timelinerecord"
                component={Timelinerecord}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="RecordEdit"
                component={RecordEdit}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="Community"
                component={Community}
                options={{ headerShown: false }}
              />
              <Stack.Screen
                name="Mypage"
                component={Mypage}
                options={{ headerShown: false }}
              />
            </Stack.Navigator>
          ) : null}
        </NavigationContainer>
      </ApplicationProvider>
    </>
  );
};
export default App;
