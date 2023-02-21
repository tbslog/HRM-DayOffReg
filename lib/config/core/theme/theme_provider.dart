import 'package:flutter/material.dart';

class ThemeProvider extends ChangeNotifier {
  ThemeMode themeMode = ThemeMode.dark;

  bool get isDarkMode => themeMode == ThemeMode.dark;

  void toggleTheme(bool isOn) {
    themeMode = isOn ? ThemeMode.dark : ThemeMode.light;
    notifyListeners();
  }
}

/////// Han che de Opacity !

class MyThemes {
  static final darkTheme = ThemeData(
      indicatorColor: const Color(0xffF9D205),
      scaffoldBackgroundColor: const Color(0xff212629),
      backgroundColor: const Color(0xFFE5E5E5),
      primaryColor: Colors.white,
      primaryColorDark: Colors.black,
      primaryColorLight: const Color(0xffFFFBFB),
      cardColor: const Color.fromARGB(255, 78, 78, 78),
      colorScheme: const ColorScheme.dark(),
      iconTheme: const IconThemeData(
          color: Color.fromARGB(255, 216, 187, 39))); //// han che opacity
  // iconTheme: const IconThemeData(
  //     color: iconMenu, opacity: 0.8)); //de ocpacity la 0 de test lag
  // );
  static final lightTheme = ThemeData(
      indicatorColor: const Color(0xffF97F7F),
      scaffoldBackgroundColor: Colors.white,
      backgroundColor: Colors.grey.shade400,
      primaryColor: Colors.grey.shade600,
      primaryColorDark: const Color(0xffEDF0F3),
      primaryColorLight: const Color(0xffFFFFFF),
      cardColor: Colors.white,
      colorScheme: const ColorScheme.light(),
      iconTheme: const IconThemeData(
        color: Colors.amber,
      ));
  // iconTheme: const IconThemeData(color: iconMenu, opacity: 0.8));
  // );
}
