// Placeholder for database helper (use sqflite or drift in real app).
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class AppDatabase {
  static Database? _instance;

  static Future<Database> open() async {
    if (_instance != null) return _instance!;
    final path = join(await getDatabasesPath(), 'udin_kasir.db');
    _instance = await openDatabase(path, version: 1, onCreate: (db, v) async {
      await db.execute('''
        CREATE TABLE users(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT,
          password_hash TEXT,
          role TEXT,
          created_at TEXT
        );
      ''');
      // add other tables as needed
    });
    return _instance!;
  }
}
