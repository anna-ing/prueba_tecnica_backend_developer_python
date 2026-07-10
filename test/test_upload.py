
def test_upload_without_file(client):
    response = client.post("/cbam/upload")

    assert response.status_code == 422

def test_upload_valid_excel(client):
    with open("test/files/CBAM_Shared_Data_Intake_Template_filled.xlsx", "rb") as f:
        response = client.post(
            "/cbam/upload",
            files={
                "file": (
                    "CBAM_Shared_Data_Intake_Template_filled.xlsx",  
                    f,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            }
        )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200