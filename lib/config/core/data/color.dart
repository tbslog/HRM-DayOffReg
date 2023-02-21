import 'package:flutter/material.dart';

class CustomColor {
  // COlor
  static const Color backgroundAppbar = Color(0xFFF9A825);
  static const Color colorTitle = Color(0xFF000000);
  static const Color borderColor = Color(0xFFF3BD60);
  static const Color colorPrimary = Color(0xFF000000);
  static const Color backgroundLight = Color(0xFFFFFFFF);
  static const Color colorButton = Color(0xFF3498DB);

  //gradient
  static const Gradient gradient = LinearGradient(
    colors: [
      Color(0xFFF3BD60),
      Colors.white,
    ],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    stops: [0.4, 0.8],
  );
}
