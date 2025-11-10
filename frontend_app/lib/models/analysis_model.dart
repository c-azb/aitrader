
class AnalysisModel {
  final String? managerResponse;
  final String? base64Image;
  final String? graphError;

  AnalysisModel(
    this.managerResponse,this.base64Image,this.graphError
  );

  Map<String, dynamic> toJson() {
    return {
      'manager_response': managerResponse,
      'chart_img': base64Image,
      'graph_error': graphError,
    };
  }
}