import 'package:flutter/material.dart';
import 'package:frontend_app/home_page.dart';
import 'package:frontend_app/themes/main_theme.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Stocks Analysis',
      theme: ThemeData(
        colorScheme: getMainTheme(),
      ),
      debugShowCheckedModeBanner: false,
      home: const HomePage()
    );
  }
}

