import 'package:flutter/material.dart';
import 'package:frontend_app/about.dart';

void onClickAbout(BuildContext context){
  final route = ModalRoute.of(context);
  String? currentRouteName = route?.settings.name;

  if (currentRouteName == null){
    return;
  }

  Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => AboutPage()),
    );
    //    Navigator.pushNamed(context, '/secondScreen'); //Register page...
}

AppBar mainAppBar(String title,BuildContext context) {
  return AppBar(
    title: Text(
      title,
      style: TextStyle(fontWeight: FontWeight.bold, fontSize: 22),
    ),
    backgroundColor: Theme.of(context).colorScheme.primaryFixedDim,
    centerTitle: true,
    actions: [
      Container(
        margin: EdgeInsets.all(5),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.shadow,
          borderRadius: BorderRadius.circular(5)
        ),
        child: IconButton(onPressed: ()=>{ onClickAbout(context) }, icon: Icon(Icons.menu_book))
        )
    ],
  );
}
