import 'dart:convert';

// import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
// import 'package:frontend_app/models/analysis_model.dart';
import 'package:frontend_app/widgets/app_bar.dart';
import 'package:frontend_app/widgets/dialog_alert.dart';
import 'package:gpt_markdown/gpt_markdown.dart';
import 'package:http/http.dart' as http;

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController myController = TextEditingController();
  bool isLoading = false;
  String managerResponse = '';
  String chartImage = '';

  Future<void> testAPIConnection() async {
    try {
      final response = await http.get(
      Uri.parse('http://127.0.0.1:8000')
    );
    if(response.statusCode != 200){
      showAlertDialog('Failed to connect to the AI...','Connection Error',context);
    }
    } catch (e) {
      showAlertDialog('Failed to connect to the AI...','Connection Error',context);
    }
  }

  Future<void> onClickSearch() async {
    if (myController.text.isEmpty){
      showAlertDialog('Ticker symbol is empty','Invalid input text',context);
      return;
    }

    setState(() {isLoading=true;});

    final Map<String, dynamic> data = {'ticker_symbol': myController.text};
    myController.text = '';

    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/trader_agent'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(data),
    );

    if(response.statusCode == 200){
      final responseJson =json.decode(response.body);
      setState(() {
        managerResponse = responseJson['manager_response'].toString();
        chartImage = responseJson['chart_img'].toString();
      });
      
    }else{
      showAlertDialog('Failed to generate the answer, try again later...','Response Error',context);
    }

    setState(() {isLoading=false;});
    
  }

  @override
  void initState() {
    super.initState();
    // testAPIConnection(context);
  }

  

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: mainAppBar('Home', context),
      body: SingleChildScrollView(
        child: Column(
          children: [
            startText(context),
            inputTextRequest(context, myController, onClickSearch),
            if (isLoading)
              loadingContainer(context),
            if (managerResponse.isNotEmpty)
              analysisDisplay(),
              if (chartImage.isNotEmpty)
                chartDisplay()
          ],
        ),
      ),
    );
  }

  Column chartDisplay() {
    return Column(
      children: [
        Container(
          margin: EdgeInsets.only(top: 35,bottom: 10),
          child: Text("Finance Asset Chart",style: TextStyle(fontSize: 26,fontWeight: FontWeight.bold)),
        ),
        Center(
          child: Image.memory(
              base64Decode(chartImage),
              // width: 200, // Optional: specify width
              // height: 200, // Optional: specify height
              fit: BoxFit.cover, // Optional: specify how the image should be fitted
            ),
        ),
      ],
    );
  }

  Column analysisDisplay() {
    return Column(
              children: [
                Container(
                  margin: EdgeInsets.only(top:30,bottom: 10),
                  child: Text(
                    "AI Analysis",
                    textAlign: TextAlign.justify,
                    style: TextStyle(fontWeight: FontWeight.bold,fontSize: 18),
                    ),
                ),
                Container(
                  margin: EdgeInsets.only(right: 20,left: 20),
                  padding: EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    border: BoxBorder.all(),borderRadius: BorderRadius.circular(10)
                  ),
                  child: GptMarkdown(
                    managerResponse,
                    textAlign: TextAlign.justify,
                    ),
                ),
              ],
            );
  }

  Container loadingContainer(BuildContext context) {
    return Container(
              alignment: Alignment.centerLeft,
              margin: EdgeInsets.all(30),
              padding: EdgeInsets.all(10),
              child: Row(
                children: [
                  SpinKitCircle(
                    color: Theme.of(context).colorScheme.primary,
                    size: 20,
                  ),
                  SizedBox(width: 5),
                  Text("Analysing"),
                ],
              ),
            );
  }

  Container inputTextRequest(
    BuildContext context,
    TextEditingController myController,
    Future<void> Function() onClickSearch,
  ) {
    return Container(
      margin: EdgeInsets.only(top: 30, left: 30, right: 30),
      decoration: BoxDecoration(
        boxShadow: [
          BoxShadow(
            color: Theme.of(context).colorScheme.shadow,
            blurRadius: 5,
            spreadRadius: 1,
          ),
        ],
      ),

      child: TextField(
        controller: myController,
        maxLength: 10,
        decoration: InputDecoration(
          counterText: '',
          filled: true,
          fillColor: Theme.of(context).colorScheme.surface,
          hintText: "AAPL",
          hintStyle: TextStyle(color: Theme.of(context).colorScheme.shadow),
          suffixIcon: IconButton(
            onPressed: () => {onClickSearch()},
            icon: Icon(Icons.search),
          ),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(5),
            borderSide: BorderSide.none,
          ),
          contentPadding: EdgeInsets.all(15),
        ),
      ),
    );
  }

  Container startText(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(10),
      margin: EdgeInsets.only(top: 30, right: 20, left: 20),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.primaryContainer,
        borderRadius: BorderRadius.circular(2),
      ),
      child: Text(
        "Welcome to AI finance analyst! Enter financial ticker symbols like stocks to request an analysis!",
        textAlign: TextAlign.center,
      ),
    );
  }
}
