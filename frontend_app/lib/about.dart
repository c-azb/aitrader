
import 'package:flutter/material.dart';
import 'package:frontend_app/widgets/app_bar.dart';

class AboutPage extends StatelessWidget {
  const AboutPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: mainAppBar('About', context),
      body: Container(
        margin: EdgeInsets.all(30),
        padding: EdgeInsets.all(10),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.shadow,
          borderRadius: BorderRadius.circular(10)
        ),
        child: Wrap(
          children: [
            Text(
              ("This is a generative AI application that is capable of doing finance research about a specific tickersymbol.\n"
               "The reaserch is made in two steps, one by a fundamentals AI analyst and a technical analysis AI analyst."
              ),
              textAlign: TextAlign.center
            ),
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: Text(
                ("Disclaimer:\n"
                "Investing is risky and all recommendations made by this application should be treaded as education only."
                ),
                textAlign: TextAlign.center,
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
      ),
    );
  }
}