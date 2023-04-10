// ignore_for_file: constant_identifier_names

class AppConstants {
  static const String THEME_KEY = "dark";

  //api
  static const int RESPONSE_CODE_SUCCESS = 200;
  static const int RESPONSE_CODE_ERROR = 400;
  static const int RESPONSE_CODE_SERVER_ERROR = 500;
  static const String KEY_ACCESS_TOKEN = "access_token";

  //Role
  static const String KEY_ROLE = "role";
  static const String KEY_IMAGE = "image";
  static const String KEY_ID_USER = "id_user";
  static const String KEY_ID_KH = "id_kh";
  static const String KEY_ID_MABOPHAN = "id_bophan";
  static const String KEY_ID_MANV = "id_NV";

  // Url

  // static const String urlBase = "http://103.149.28.137:300";
  // static const String urlBase = "http://192.168.0.76:300";
  static const String urlBase = "http://tlogapi.tbslogistics.com.vn:202";
  // static const String urlBase = "http://192.168.0.45:300";

  // Url Client
  //Tài xế
  static const String createPhieuvao = "createphieuvaocong";

  //List url
  // create_leave
  static const String urlListOffType = "dayOffType";
  static const String urlRegister = "day-off-letter";
}
