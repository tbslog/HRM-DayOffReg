import 'package:flutter/material.dart';

class CustomTextStyle {
  //style title
  static const TextStyle tilteAppbar = TextStyle(
    fontSize: 18,
    color: Colors.white,
    fontWeight: FontWeight.bold,
  );
  //style primary
  static const TextStyle titlePrimary = TextStyle(
    fontSize: 16,
    color: Colors.black,
    fontWeight: FontWeight.bold,
  );
  static const TextStyle textPrimary = TextStyle(
    fontSize: 15,
    color: Color(0xFF3498DB),
    fontWeight: FontWeight.normal,
  );
  static textFormFieldStyle(String label, String hint) {
    return InputDecoration(
      labelText: label,
      hintText: hint,
      alignLabelWithHint: true,
      contentPadding: const EdgeInsets.symmetric(vertical: 5),
      labelStyle: const TextStyle(
        color: Colors.black,
        // fontSize: 24,
      ),
      floatingLabelStyle: const TextStyle(
        color: Colors.black,
        fontSize: 24,
      ),
      enabledBorder: const UnderlineInputBorder(
        borderSide: BorderSide(
          color: Colors.black,
        ),
      ),
      focusedBorder: const UnderlineInputBorder(
        borderSide: BorderSide(color: Colors.black, width: 2),
      ),
    );
  }
}
